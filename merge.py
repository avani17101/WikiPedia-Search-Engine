#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Avani
"""
from collections import defaultdict
import heapq
import math

size = 5*1024*1024
ptr_dict = defaultdict(dict)
word_dict = defaultdict(dict)


def make_dict(line, heap, fs):
    line = line.strip().split("/")
    if line[0] in word_dict:
        l = line[1]
        li = []
        l = l.split(";")
        li.append(l)
        var = True
        for i in l:
            j = i.split("-")
            x = int(j[0])
            y = j[1]
            word_dict[line[0]][x] = y
        return var
    else:
        heapq.heappush(heap, line[0])
        var = False
        ptr_dict[line[0]] = fs
        li = []
        l = line[1]
        l = l.split(";")
        li.append(l)
        for i in l:
            j = i.split("-")
            x = int(j[0])
            y = j[1]
            word_dict[line[0]][x] = y
        return var


def write_dict(word, fp):
    line = ""
    line = line+word+"/"
    l = list(word_dict[word])
    l.sort()
    for i in l:
        line = line+str(i)
        line += "-"
        line += word_dict[word][i]+";"
    line = line[:-1]
    fp.write(line)
    fp.write("\n")


def remove_dict(word):
    ptr_dict.pop(word)
    word_dict.pop(word)


def merge_files(fname, no_files):
    global ptr_dict
    global file_dict
    global size
    count = 0
    fp = open("tmp/file"+str(count), "w")
    fo = open("tmp/offset", "w")
    heap = []

    # fill first entry in heap from all files
    for i in range(0, no_files):
        file = fname+str(i)
        fs = open(file, "r")
        line = fs.readline()
        while line != '' and make_dict(line, heap, fs):
            line = fs.readline()

    while len(heap) > 0:
        word = heapq.heappop(heap)
        f_ptr = ptr_dict[word]
        write_dict(word, fp)
        if fp.tell() >= size:
            fp.close()
            off_entry = word+":"+str(count)+"\n"
            fo.write(off_entry)
            count = count+1
            fp = open("tmp/file"+str(count), "w")
        remove_dict(word)
        line = f_ptr.readline()
        while line != '' and make_dict(line, heap, f_ptr):
            line = f_ptr.readline()
    fp.close()
    fo.write(word+":"+str(count)+"\n")
    fo.close()


def main():
    file_no = 978
    merge_files("tmp/temp",file_no)



    '''count = merge_files("tmp/temp",1000,2000,count)
    count = merge_files("tmp/temp",2000,3000,count)
    merge_files("tmp/temp",3000,3913,count)'''

if __name__ == "__main__":  
    main()
