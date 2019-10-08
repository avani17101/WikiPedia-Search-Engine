# WikiPedia-Search-Engine
Search  engine for wikipedia

Utility
WikiIndexer.py- parses wikipedia dump and makes inverted index
merge.py- merges index files and split them into smaller chunks
search.py- main query program that returns results in less than 5 seconds

Steps
Create a folder named Temp in WikiPedia Seach Engine folder.

Run the following commands

python WikiIndexer.py <absolute path of data>
  
python search.py <absolute path of folder where indexed files stored>
  
  and fire queries to get search results.
