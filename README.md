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

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e spacy

This command will generate 2 file: **wowool-vs-spacy-tbl.txt** and **wowool-vs-spacy-diff.txt**

* wowool-vs-spacy-tbl.txt  : Print out a table with the entities side by side 
* wowool-vs-spacy-diff.txt : : Perfoming a diff beween the two diff restul files


### Results

#### Anaphora

    python3 -m nlp_compare -e spacy -l english -p "english,entity" -f tests/data/anaphora.text

As we can see spacy is missing all the references in the second sentence  **Mary Smith** (*she*), **EyeOnText** ( *the it company* )  and **John Dow** (*he*)

`John Dow and Mary Smith went to work at EyeOnText.`

|   beg |   end | uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------|------------------|-------------------|
|     0 |     8 | PERSON    | John Dow   | PERSON           | John Dow          |
|    13 |    23 | PERSON    | Mary Smith | PERSON           | Mary Smith        |
|    40 |    49 | ORG       | EyeOnText  | ORG              | EyeOnText         |


`She works for the it company but he only cleans there.`

|   beg |   end | uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------|------------------|-------------------|
|    51 |    54 | PERSON    | Mary Smith | **Missing**      |                   |
|    65 |    79 | ORG       | EyeOnText  | **Missing**      |                   |
|    84 |    86 | PERSON    | John Dow   | **Missing**      |                   |


#### Wrong tagging

As we can see spacy is wrongly tagging **the George Washington** missing **John Smith** and missing the location **Washington** from *longtime Washington lawyer*

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

|   beg |   end | uri_wow     | text_wow      | uri_spacy        | text_spacy            |
|-------|-------|-------------|---------------|------------------|-----------------------|
|     0 |    10 | PERSON      | John Smith    | PERSON           | John Smith            |
|    12 |    33 | **Missing** |               | PERSON           | the George Washington |
|    23 |    33 | LOC         | Washington    | **Missing**      |                       |
|    52 |    65 | PERSON      | Eugene Fidell | PERSON           | Eugene Fidell         |
|    78 |    88 | LOC         | Washington    | GPE              | Washington            |
|    78 |    88 | GPE         | Washington    | **Missing**      |                       |


`He worked with the president George Washington.`

|   beg |   end | uri_wow   | text_wow          | uri_spacy        | text_spacy        |
|-------|-------|-----------|-------------------|------------------|-------------------|
|    97 |    99 | PERSON    | John Smith        | **Missing**      |                   |
|   126 |   143 | PERSON    | George Washington | PERSON           | George Washington |
|   133 |   143 | LOC       | Washington        | **Missing**      |                   |


#### Conjecture


As we can see spacy is wrongly tagging **Miyaktama** wrongly the the second sentence as a organization.
But it clear from the first sentence that it is a Person.

`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------------|------------------|-------------------|
|     4 |    20 | PERSON    | Miyaktama Mitshu | PERSON           | Miyaktama Mitshu  |


`Miyaktama is a very good leader.`

|   beg |   end | uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------------|------------------|-------------------|
|    50 |    59 | PERSON    | Miyaktama Mitshu | ORG              | Miyaktama         |


#### Spacy demo sample data.

We are testing the sample sentences in the site of Displacy

In this first sentence, the references to *the company* and *him* are lost in spacy.

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

|   beg |   end | uri_wow   | text_wow        | uri_spacy        | text_spacy        |
|-------|-------|-----------|-----------------|------------------|-------------------|
|     5 |    20 | PERSON    | Sebastian Thrun | PERSON           | Sebastian Thrun   |
|    61 |    67 | ORG       | Google          | ORG              | Google            |
|    71 |    75 | CARDINAL  | 2007            | DATE             | 2007              |
|    98 |   109 | ORG       | Google          | **Missing**      |                   |
|   115 |   118 | PERSON    | Sebastian Thrun | **Missing**      |                   |


The reference to *Thrun*, who is mentioned in the previous sentence, is lost and the name is wrongly identified as a location. Spacy is also missing *Udacity* as a company, whereas it is clearly identified as a startup.

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

|   beg |   end | uri_wow     | text_wow        | uri_spacy        | text_spacy        |
|-------|-------|-------------|-----------------|------------------|-------------------|
|   270 |   275 | PERSON      | Sebastian Thrun | GPE              | Thrun             |
|   339 |   346 | ORG         | Udacity         | **Missing**      |                   |
|   369 |   375 | ORG         | Recode          | ORG              | Recode            |
|   376 |   393 | **Missing** |                 | DATE             | earlier this week |


## Stanza vs Wowool

### Setup

    pip install stanza

### Comparing

Using this command you will see the comparison between stanza and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e stanza --show

This command will generate 2 file: **wowool-vs-stanza-tbl.txt** and **wowool-vs-stanza-diff.txt**

* wowool-vs-stanza-tbl.txt  : Print out a table with the entities side by side 
* wowool-vs-stanza-diff.txt : : Perfoming a diff beween the two diff restul files

#### Anaphora

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/anaphora.txt

Wowool startup time: 0.247
Stanza startup time: 8.582
Processing time of stanza: 0.701 Counter({'PERSON': 2, 'ORG': 1})
Processing time of wowool: 0.010 Counter({'PERSON': 4, 'ORG': 2})
wowool is 73.213 faster than stanza

As we can see stanza is missing all the references in the second sentence  **Mary Smith** (*she*), **EyeOnText** ( *the it company* )  and **John Dow** (*he*)

`John Dow and Mary Smith went to work at EyeOnText.`

|   beg |   end | uri_wow   | text_wow   | uri_stanza   | text_stanza   |
|-------|-------|-----------|------------|--------------|---------------|
|     0 |     8 | PERSON    | John Dow   | PERSON       | John Dow      |
|    13 |    23 | PERSON    | Mary Smith | PERSON       | Mary Smith    |
|    40 |    49 | ORG       | EyeOnText  | ORG          | EyeOnText     |


`She works for the it company but he only cleans there.`

|   beg |   end | uri_wow   | text_wow   | uri_stanza   | text_stanza   |
|-------|-------|-----------|------------|--------------|---------------|
|    51 |    54 | PERSON    | Mary Smith | **Missing**  |               |
|    65 |    79 | ORG       | EyeOnText  | **Missing**  |               |
|    84 |    86 | PERSON    | John Dow   | **Missing**  |               |


#### Wrong tagging

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/person_wrong_names.txt

As we can see spacy is wrongly tagging **George Washington** as a location and missing **John Smith** and missing the location **Washington** from *longtime Washington lawyer*

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

|   beg |   end | uri_wow     | text_wow      | uri_stanza   | text_stanza       |
|-------|-------|-------------|---------------|--------------|-------------------|
|     0 |    10 | PERSON      | John Smith    | PERSON       | John Smith        |
|    16 |    33 | **Missing** |               | GPE          | George Washington |
|    23 |    33 | LOC         | Washington    | **Missing**  |                   |
|    52 |    65 | PERSON      | Eugene Fidell | PERSON       | Eugene Fidell     |
|    78 |    88 | LOC         | Washington    | GPE          | Washington        |
|    78 |    88 | GPE         | Washington    | **Missing**  |                   |


`He worked with the president George Washington.`

|   beg |   end | uri_wow   | text_wow          | uri_stanza   | text_stanza       |
|-------|-------|-----------|-------------------|--------------|-------------------|
|    97 |    99 | PERSON    | John Smith        | **Missing**  |                   |
|   126 |   143 | PERSON    | George Washington | PERSON       | George Washington |
|   133 |   143 | LOC       | Washington        | **Missing**  |                   |

#### Conjecture


    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/person_conjecture.txt

Stanza is doing better the spacy in this case, but still lozes the reference to * Miyaktama Mitshu*.

`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza      |
|-------|-------|-----------|------------------|--------------|------------------|
|     4 |    20 | PERSON    | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu |


`Miyaktama is a very good leader.`

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza   |
|-------|-------|-----------|------------------|--------------|---------------|
|    50 |    59 | PERSON    | Miyaktama Mitshu | PERSON       | Miyaktama     |


#### Spacy demo sample data.

╰─❯ python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/companies.txt
wowool is 96.824 faster than stanza

In this case stanza split the name *Sebastian Thrun* in two Person, where it is just one. They are missing `Google` and `him` 

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

|   beg |   end | uri_wow     | text_wow        | uri_stanza   | text_stanza   |
|-------|-------|-------------|-----------------|--------------|---------------|
|     5 |    20 | PERSON      | Sebastian Thrun |              |               |
|     5 |    14 |             |                 | PERSON       | Sebastian     |
|    15 |    20 |             |                 | PERSON       | Thrun         |
|    61 |    67 | ORG         | Google          | ORG          | Google        |
|    71 |    75 | CARDINAL    | 2007            | DATE         | 2007          |
|    98 |   109 | ORG         | Google          | **Missing**  |               |
|   115 |   118 | PERSON      | Sebastian Thrun | **Missing**  |               |

Here they do capture `Udacity` but are wrongly assinging Recode as a **WORK_OF_ART**

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

|   beg |   end | uri_wow     | text_wow        | uri_stanza   | text_stanza       |
|-------|-------|-------------|-----------------|--------------|-------------------|
|   270 |   275 | PERSON      | Sebastian Thrun | PERSON       | Thrun             |
|   339 |   346 | ORG         | Udacity         | ORG          | Udacity           |
|   369 |   375 | ORG         | Recode          | WORK_OF_ART  | Recode            |


## Conclusions

In this project, we compared various Natural Language Processing (NLP) models to evaluate their performance on different tasks. The key findings are as follows:

Afther lowering our range of annotation and removing the attribute information that is part of the annotations like (sector, gender, postion, headquarters, key_people and many more )


* **Speed**: Wowool has similar speed as Spacy but returning much richer information. but Wowool has a much faster starup time. Stanza the very slow in comparizon, startup speed and processing speed, sometime up to 100 time slower.


* **Accurary**: It is very clear that Wowool knows about language and tackels all the linguistic issues that machine learning engine cannot tackel, like anaphora, conjecture, hyphenation, instantance, name references and many more. 


### Resource Utilization


