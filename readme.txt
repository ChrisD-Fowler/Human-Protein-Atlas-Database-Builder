INTRODUCTION: 

Welcome to my first attempt to write a program to parse JSON data and write to an SQL database. The purpose of this program is to help myself learn Python coding, particularly data structures.

Although the database is not exhaustive, I believe it has enough tables and rows to illustrate comprehension of the basics of sound database design. If you are a fellow programming student, I hope this can help you in some way - good luck in your studies! 

-- Christopher Fowler (c.fowler00@yahoo.com)

--------------------------------------

HOW TO USE:

1) Download the applicable JSON data for The Human Atlas Project from: https://www.proteinatlas.org/about/download

2) Place the .json file in the same directory as atlasload.exe

3) Run the program and follow the prompts! You will have to input the name of your JSON file and specify the name of the database it will output. After that, the program will complete the rest.

4) Once complete, you may now open and view the resulting .sqlite database with the program of your choice (i.e., SQLite).

Enjoy! This was made for use ONLY with the JSON downloadable from The Human Atlas Project and will not work with any other data.

--------------------------------------

Proteins Table

PK: prot_id INTEGER
FK: gene_name VARCHAR
position VARCHAR
chromosome VARCHAR
prot_class VARCHAR
Genes Table

PK: gene_id INTEGER
gene_name VARCHAR
ens_desc VARCHAR
gene_desc VARCHAR
uniprot VARCHAR
Prognostics Table

PK: prog_id INTEGER
FK: gene_name VARCHAR
prog_name VARCHAR
prog_type VARCHAR
p_val FLOAT
is_prog BOOLEAN


