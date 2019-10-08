import xml.sax
import re
from Stemmer import Stemmer
from collections import defaultdict
import timeit
import math
#from merge import merge_files
import sys

words= defaultdict(dict)
stopwords= defaultdict(int)
title_dict=defaultdict(str)
fp_title_offsetfile=None
file_no=0
file_no_title=0
no_of_docs=0

with open ('stop_words.txt','r') as f:
    pi=0
    for i in f:
        i=i.strip(' ').strip("\n")
        stopwords[i]=1
    pi+=1



def removeStopWords(dataList):
    temp=[key for key in dataList if stopwords[key]!=1]
    return temp

def tokenise(data):
    tok=[]
    tok=re.findall(r'[a-z]+',data)
    return tok
    

def stem(datalist):                                          #Stemming
    stemmer=Stemmer("english")
    tmp=[]
    for x in datalist:
        y=stemmer.stemWord(x)
        tmp.append(y)
    return tmp

def makeDict(datalist):
      datalist = removeStopWords(datalist)
      p=[]
      temp=defaultdict(int)
      datalist= stem(datalist)
      
      for x in datalist:
        temp[x]=temp[x]+1
      
      return temp

def findExternalLinks(data):
  line = data.split("==external links==")
  links=[]
  if len(line)>=2:
    lines=[]
    lines=line[1].split("\n")
    length=len(lines)
    for i in range(length):
      if '* [' in lines[i] or '*[' in lines[i]:
        temp=[]
        temp=lines[i].split(' ')
        word=""
        word=[key for key in temp if 'http' not in temp]
        word=' '.join(word).encode('utf-8')
        links.append(word)
  links=tokenise(b' '.join(links).decode())
  #print(links)
  tmp=makeDict(links)
  return tmp

def writeFile(fname):
    global words
    with open("tmp/"+fname,'w') as f:
        li=sorted(words.keys())
        #print(words.keys())
        for w in (li):
            s=""
            s=s+w+"/"
            tmp=words[w]
            for j in (sorted(tmp.keys())):
                s=s+str(j)+"-"
                
                tot_words_in_doc=0
                for k in range(0,5):
                    tot_words_in_doc+=words[w][j][k]
                
                #s=s+"tf"+str(1+round(math.log10(tot_words_in_doc),4))+":"
                
                s=s+"f"+str(tot_words_in_doc)+":"
                
                if words[w][j][0]>0:
                    s=s+"t"+str(words[w][j][0])+":"
                if words[w][j][1]>0:
                    s=s+"b"+str(words[w][j][1])+":"
                if words[w][j][2]>0:
                    s=s+"i"+str(words[w][j][2])+":"
                if words[w][j][3]>0:
                    s=s+"c"+str(words[w][j][3])+":"
                if words[w][j][4]>0:
                    s=s+"e"+str(words[w][j][4])+":"
                s=s[:-1]
                s=s+";"
            s=s[:-1]
            f.write(s)
            f.write("\n")
            
def writeTitle(fname):
     global title_dict
     global file_no_title
     global fp_title_offsetfile
     with open("tmp/"+fname,'w') as f:
        li=sorted(title_dict.keys())
        fp_title_offsetfile.write(str(li[0]))
        fp_title_offsetfile.write(" "+str(file_no_title)+"\n")
        for doc_id in (li):
            f.write(str(doc_id))
            f.write("-"+str(title_dict[doc_id])+"\n")
    
def processTitle(data):
    data=data.lower()
    data_tok=re.findall(r'\d+|[\w]+',data)
    temp=makeDict(data_tok)
    return temp    

def process_Text(data):
    data=data.lower()
    ext=findExternalLinks(data)
    body_text=[]
    info_box=[]
    category=[]
    data = data.replace('_',' ').replace(',','')
    l=data.split('\n')
    i=0
    body_fin=1
    co=0
    lengt=len(l)
    while i < lengt:
        if '{{infobox' in l[i]:
            p=[]
            temp=l[i].split('{{infobox')
            co=co+temp[1].count('{{')-temp[1].count('}}')
            co=co+1
            info_box.append(temp[1])
            body_text.append(temp[0])
            i=i+1
            while co>=1 and i<len(l):
                co=co+l[i].count('{{')-l[i].count('}}')
                info_box.append(l[i])
                i=i+1
        elif body_fin==1:
            body_text.append(l[i])
            if '[[category' in l[i] or '==external links==' in l[i]:
                body_fin=0
        else:
            if '[[category' in l[i]:
                temp=l[i].replace('[[category:','')
                category.append(temp)
        i=i+1
    
    cat=tokenise(' '.join(category))
    body=tokenise(' '.join(body_text))
    info=tokenise(' '.join(info_box))
    
    cat_n=makeDict(cat)
    body_n=makeDict(body)
    info_n=makeDict(info)
    
    return cat_n,body_n,info_n,ext
   
    

class WikiHandler( xml.sax.ContentHandler):
    
    def __init__(self):
        self.page=0
        self.id=0
        self.text=0
        self.title=0
        self.count=0
        self.count_title=0
        self.bufid=""
        self.title_words=defaultdict(int)
        self.cat_words=defaultdict(int)
        self.body_words=defaultdict(int)
        self.infobox_words=defaultdict(int)
        self.extLinks_words=defaultdict(int)
    
    def makeIndex(self,buffid,title,cat,body,info,ext):
        
        global file_no
        global file_no_title
        global title_dict
        
        c=float(len(cat))
        tmp=defaultdict(int)
        t=float(len(title))
        
        allWordsList=set(title.keys())
        for i in ext.keys():
            allWordsList.add(i)
        li_co=0
        
        for i in cat.keys():
            allWordsList.add(i)
         
        li_co+=1    
        global words
        
        for i in body.keys():
            allWordsList.add(i)
        
        
        for i in info.keys():
            allWordsList.add(i)
        
        b=float(len(body))
        li_co+=1
        inf=float(len(info))
        li_co+=1
        e=float(len(ext))
        
        px=0
        for i in allWordsList:
            l=[]
            px+=1
            
            l.append(title[i])
            l.append(body[i])
            l.append(info[i])
            l.append(cat[i])
            l.append(ext[i])
            
            words[i][int(self.bufid)]=l
        
        if self.count > 20000 :
            writeFile("temp"+str(file_no))
            self.count=0
            file_no=file_no+1
            words=defaultdict(dict)
            
        if self.count_title > 20000:
            writeTitle("title"+str(file_no_title))
            title_dict=defaultdict(str)
            file_no_title+=1
            self.count_title=0
        
    def startElement(self,tag,attr):
        global no_of_docs
        if(tag=="id" and self.page==0):
            self.page=1
            self.id=1
            self.bufid=""
            no_of_docs+=1
        elif(tag=="title"):
            self.title=1
            self.buftitle=""
        elif(tag=="text"):
            self.text=1
            self.buftext=""
            
    def characters(self,data):
        if (self.id==1 and self.page==1):
            self.bufid += data
            title_dict[int(self.bufid)]=self.buftitle
            #s=self.bufid+" "+self.buftitle+"\n"
            #fp_titlefile.write(s)
        elif(self.title==1 ):
            self.buftitle += data
        elif(self.text==1):
            self.buftext += data
       
                     
    def endElement(self,tag):
        #global fp_titlefile
        if(tag=="page"):
            self.page=0
            self.count+=1
            self.count_title+=1
        if(tag=="title"):
            self.title=0
            self.title_words=processTitle(self.buftitle)
        if(tag=="id"):
            self.id=0
        if(tag=="text"):
            self.text=0
            self.cat_words,self.body_words,self.infobox_words,self.extLinks_words=process_Text(self.buftext)
            tmp=[]
            WikiHandler.makeIndex(self,self.bufid,self.title_words,self.cat_words,self.body_words,self.infobox_words,self.extLinks_words)
            

def main():
    global fp_title_offsetfile
    fp_title_offsetfile=open("tmp/title_offset","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse(sys.argv[1])
    print("no_of_docs"+str(no_of_docs))
    fi= open("tmp/doc_count.txt","w+")
    fi.write(str(no_of_docs))
    fi.close()
    writeFile("temp"+str(file_no))
    writeTitle("title"+str(file_no_title))
    fp_title_offsetfile.close()
    #merge_files("tmp/temp",file_no+1)

        
        
if __name__ == "__main__":                                            #main
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print (stop - start)
