# Datasetify
Automatically create a dataset of NLP features from a plain text file

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

# Purpose
In my work as an NLP developer and as a Data Science student at the University of Washington I often find myself in need of datasets that extract preliminary NLP features from text like sentiment, typology and useful
grammar patterns. This simple project can extract those features from any plain text and create a CSV file for you. If you're working with larger text corpura it might be helpful to instantiate multiple classes and use multithreading. 

  - Create a csv file suitable for data science experiments of processed text
  - extract relevant NLP features from a text

### Installation
Install requirements for Python 2:
```sh
$ pip install -r requirements.txt
```

Install requirements for Python 3:
```sh
$ pip3 install -r requirements.txt
```
#### Creating a dataset is as simple as calling the function with a text file

```
create_dataset("plain-text-file.txt")
```
### Sample output

```
   Nouns  Sentiment Typology  Verbs  Word Count
0      8    -0.4000      SVO      2          17
1     12    -0.2000      SVO      4          29
2      8     0.0000      VSO      5          28
3      4     0.0000      VSO      2          15
4     26     0.0385      SVO      7          77
5      8     0.0000      SVO      4          20
6      3     0.1250      VSO      0          12
7     13     0.1389      SVO      2          35
8      3     0.0000      SVO      2          10
9     15    -0.1250      SVO      1          32
```

License
----

MIT


**Free Software, Hell Yeah!**
