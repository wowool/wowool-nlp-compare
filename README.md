# NLP compare

This tool allows us to compare different nlp engines with the wowool engine.

## Setup

    pip install -r wowool-requirements.txt


## Spacy vs Wowool

  
### Setup

    pip install spacy
    python -m spacy download en_core_web_sm
  
### Comparing

Using this command you will see the comparison between spacy and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e spacy --show

This command will generate 2 file: **wowool-vs-spacy-tbl.txt** and **wowool-vs-spacy-diff.txt**

* wowool-vs-spacy-tbl.txt  : Print out a table with the entities side by side 
* wowool-vs-spacy-diff.txt : : Perfoming a diff beween the two diff restul files

## Stanza vs Wowool

### Setup

    pip install stanza

### Comparing

Using this command you will see the comparison between stanza and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e stanza --show

This command will generate 2 file: **wowool-vs-stanza-tbl.txt** and **wowool-vs-stanza-diff.txt**

* wowool-vs-stanza-tbl.txt  : Print out a table with the entities side by side 
* wowool-vs-stanza-diff.txt : : Perfoming a diff beween the two diff restul files
