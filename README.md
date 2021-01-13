# WikiPedia-Search-Engine
Search  engine for entire wikipedia corpus made as minor project in course taken in semester 3, Information Retrieval and Extraction course at IIIT Hyderabad.

## Utility
* WikiIndexer.py- parses wikipedia dump and makes inverted index
* merge.py- merges index files and split them into smaller chunks
* search.py- main query program that returns results in less than 5 seconds

## Data
Data used is entire wikipedia corpus which is passed in indexer, and indexed results are searched while queries.
[link](https://drive.google.com/file/d/1QMpM1CSn6j8Hwu5AabTqTQ1km9xCzSEV/view?usp=sharing)

## Steps
```bash
git clone {url of the page}
```
or
Click 'Clone or Download' on the top right hand side of the repository.

* Download the data from [here](https://drive.google.com/file/d/1QMpM1CSn6j8Hwu5AabTqTQ1km9xCzSEV/view?usp=sharing).

* Create a folder named Temp in WikiPedia Seach Engine folder.

* Run the following commands
```bash
python WikiIndexer.py <absolute path of data>
python search.py <absolute path of folder where indexed files stored>
```
* Fire queries to get search results.

**Queries** <br>
Normal search, give any words, phrases, sentences for search.

**Advanced search** <br>
Supports various field queries <br>
Use the following syntax for doing advanced search <br>
t: titlename b: words i: infobox r: references e: category  <br>

Example->  t: titlename would search the articles with <titlename>.


## Constructing the Inverted Index
* BasicStages(inorder):
* XML parsing: SAX parser used
* Data preprocessing 
: NLTK used
  * Tokenization 
  * Case folding
  * Stop words removal
  * Stemming
* Posting List / Inverted Index Creation
* Optimize

## Features:
* Support for Field Queries . Fields include Title, Infobox, Body, Category, Links, and
References of a Wikipedia page. This helps when a user is interested in searching for
the movie ‘Up’ where he would like to see the page containing the word ‘Up’ in the title
and the word ‘Pixar’ in the Infobox. You can store field type along with the word when
you index.
* Index size should be less than 1⁄4 of dump size. 
* Scalable index construction 
* Search Functionality
  * Index creation time: less than 60 secs for Java, CPP and for python it’s less than 150
secs.
  * Inverted index size: 1/4th of entire wikipedia corpus
* Advanced search as mentioned above.



## References
https://en.m.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia
