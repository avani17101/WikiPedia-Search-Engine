#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Avani
"""
import math
from collections import defaultdict
import timeit
from wikiIndexer import removeStopWords, stem, tokenise
wlist = []
tlist = []
title_dic = defaultdict(int)
opt_dict = defaultdict(int)
global no_of_docs


def get_docNum():
    global no_of_docs
    with open("tmp/doc_count.txt", "r") as fp:
        for line in fp:
            no_of_docs = int(line.strip())
            return no_of_docs
            print(no_of_docs)


no_of_docs = get_docNum()


def load_title():
    global tlist
    global title_dic
    with open("tmp/title_offsets", "r") as fp1:
        for line in fp1:
            line = line.strip().split()
            title_dic[int(line[0].strip())] = int(line[1].strip())

    fp1.close()
    tlist = sorted(list(title_dic.keys()))
    # print(title_dic)


def bsearch_titleno(docid):
    global title_dic
    global tlist
    #print(tlist)
    pos = 0
    low = 0
    high = len(tlist)-1
    # print(title_dic)
    # print(docid)
    while low <= high:
        mid = int((low+high)/2)
        if int(tlist[mid]) == docid:
            return title_dic[docid]
        elif tlist[mid] < docid:
            pos = mid
            low = mid+1
        else:
            high = mid-1
        '''print("title dic")
        print(title_dic[tlist[pos]])'''
        # print(title_dic[tlist[pos]])
        # print(title_dic[tlist[pos]])
        #print(docid,pos)
    #print(title_dic)
    return title_dic[tlist[pos]]


def get_title(fno, docid):
    global title_dic
    with open("tmp/titles"+str(fno), "r") as fp:
        for line in fp:
            line = line.split("-")
            if int(line[0]) == docid:
                # print(line[1].strip("\n"))
                return line[1].strip("\n")


def load_offsetfile():
    global opt_dict
    global wlist
    with open("tmp/offset", "r") as fp:
        for line in fp:
            line = line.strip().split(":")
            opt_dict[line[0]] = line[1]
    fp.close()
    wlist = sorted(list(opt_dict.keys()))


def bsearch_fileno(word):
    global opt_dict
    #print(opt_dict)
    global wlist
    #print(wlist)
    pos = 0
    low = 0
    high = len(wlist)-1

    while low <= high:
        mid = int((low+high)/2)
        if wlist[mid] == word:
            return opt_dict[word]
            # print(opt_dict[word])
        elif wlist[mid] < word:
            low = mid+1
        else:
            pos = mid
            high = mid-1

    # print(opt_dict[wlist[pos]])

    return opt_dict[wlist[pos]]


def getList(word, fno):
    with open("tmp/file"+str(fno), "r") as fp:
        for line in fp:
            line = line.strip().split("/")
            if line[0] == word:
                return line[1]
    return []


def rank_simple(posting_dict):
    global no_of_docs

    rank_list = defaultdict(float)
    l = posting_dict.keys()

    for word in l:
        postlist = posting_dict[word]
        if len(postlist) != 0:
            postlist = postlist.split(";")
            df = len(postlist)
            idf = math.log10(10/df)
            # print(postlist)
            for doc in postlist:
                doc = doc.split("-")
                doc_id = int(doc[0])
                line = doc[1].split(":")
                freq = int(line[0][1:])
                tf = math.log10(1+freq)
                rank_list[doc_id] += tf*idf
    # print(rank_list)
    return rank_list


def rank_field(posting_dict, query_dict):
    global no_of_docs

    rank_list = defaultdict(float)
    l = posting_dict.keys()

    wt = {'t': 140, 'i': 80, 'c': 50, 'e': 20}

    for word in l:
        postlist = posting_dict[word]
        if len(postlist) != 0:
            postlist = postlist.split(";")
            df = len(postlist)
            idf = math.log10(no_of_docs/df)
            for doc in postlist:
                doc = doc.split("-")
                doc_id = int(doc[0])
                line = doc[1].split(":")
                fields_to_match = query_dict[word]
                freq = 0
                for j in line:
                    if j[0] == 'b':
                        freq += int(j[1:])
                for i in fields_to_match:
                    for j in line:
                        if i == j[0] and i != "b":
                            freq += (int(j[1:])*wt[j[0]])
                tf = math.log10(1+freq)
                rank_list[doc_id] += tf*idf
    # print(rank_list)
    return rank_list


def simple_query(query):
    global title_dic
    # print(title_dic)
    qwords = tokenise(query)
    qwords = removeStopWords(qwords)
    qwords = stem(qwords)

    posting_dict = defaultdict(list)
    for w in qwords:
        fno = bsearch_fileno(w)
        posting = getList(w, fno)
        posting_dict[w] = posting
    ranked_list = rank_simple(posting_dict)
    if len(ranked_list) == 0:
        print("No match found")
    else:
        ranked_list_sort = sorted(
            ranked_list, key=ranked_list.get, reverse=True)
        # print(ranked_list.head())
        #print("ranked {} title {}".format(ranked_list, get_title(fno,ranked_list_sort[i])))
        for i in range(0, 10):
            if i >= len(ranked_list_sort):
                break

            fno = bsearch_titleno(ranked_list_sort[i])
            #print(fno, ranked_list_sort[i])
            print(get_title(fno, ranked_list_sort[i]))


def create_dict(qdict, line, val):
    line = tokenise(line)
    line = removeStopWords(line)
    line = stem(line)
    for i in line:
        qdict[i].append(val)
    return qdict


def get_fq_dict(inp):
    val = 0
    t, r, b, inf, c, e = "", "", "", "", "", ""
    tmpp = ""
    val = len(inp)-1
    i, tf, bf, cf, ef, rf, inff = 0, 0, 0, 0, 0, 0, 0
    while i < val:
        x = inp[i]
        y = inp[i+1]
        if "i" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 0, 0, 0, 0, 0, 1
            i = i+1
        elif "t" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 1, 0, 0, 0, 0, 0
            i = i+1
        elif "b" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 0, 1, 0, 0, 0, 0
            i = i+1
        elif "c" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 0, 0, 1, 0, 0, 0
            i = i+1
        elif "e" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 0, 0, 0, 1, 0, 0
            i = i+1
        elif "r" == x and ":" == y:
            tf, bf, cf, ef, rf, inff = 0, 0, 0, 0, 1, 0
            i = i+1
        elif tf == 1:
            t = t+x
        elif bf == 1:
            b = b+x
        elif cf == 1:
            c = c+x
        elif ef == 1:
            e = e+x
        elif rf == 1:
            r = r+x
        elif inff == 1:
            inf = inf+x
        i = i+1
    v = 1
    l = len(inp)-1
    if tf == v:
        t = t+inp[l]
    elif bf == v:
        b = b+inp[l]
    elif cf == v:
        c = c+inp[l]
    elif ef == v:
        e = e+inp[l]
    elif rf == v:
        r = r+inp[l]
    elif inff == 1:
        inf = inf+inp[l]
    qdict = defaultdict(list)
    qdict = create_dict(qdict, t, "t")
    qdict = create_dict(qdict, b, "b")
    qdict = create_dict(qdict, c, "c")
    qdict = create_dict(qdict, e, "e")
    qdict = create_dict(qdict, inf, "i")
    return qdict
    # print(qdict)


def field_query(query):
    global title_dic
    query_dict = get_fq_dict(query)

    qwords = list(query_dict.keys())

    posting_dict = defaultdict(list)
    for w in qwords:
        fno = bsearch_fileno(w)
        posting = getList(w, fno)
        posting_dict[w] = posting
        # print(posting_dict[w])
    ranked_list = rank_field(posting_dict, query_dict)

    if len(ranked_list) == 0:
        print("No match found")
    else:
        ranked_list_sort = sorted(
            ranked_list, key=ranked_list.get, reverse=True)
        for i in range(0, 10):
            if i >= len(ranked_list_sort):
                break
            fno = bsearch_titleno(ranked_list_sort[i])
            #print(fno, ranked_list_sort[i])
            print(get_title(fno, ranked_list_sort[i]))


def main():
    load_offsetfile()
    load_title()
    while True:
        print("\n\nEnter Query")
        query = input()
        query = query.lower()
        start = timeit.default_timer()
        if ("i:" in query or "b:" in query or "c:" in query or "t:" in query or "e:" in query):
            field_query(query)
        else:
            simple_query(query)
        stop = timeit.default_timer()
        print ("\ntime :- "+str(stop - start))
        # print("tilte")
        #print(get_title(943, 59341885))
        # print("bsearch")
        # print(bsearch_fileno('acd'))


main()
