# NLP compare

This tool allows us to compare different nlp engines with the wowool engine.

## Setup

    pip install -r wowool-requirements.txt


## Wowool vs Spacy,Stanza and Google

We are going to compare several cases using wowool, spacy, stanza and google NLP.

| Feature          | Wowool  | Spacy   | Stanza   | Notes                                                                                                                |
|:-----------------|:-------:|:--------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora         | Yes     | No       | No       | Stanza does not resolve pronouns like he, she, the city, the company, etc.                                          |
| Conjecture       | Yes     | No       | No       | When Mentioning a something in context, wowool will remeber that what it was later on                               |
| Aggregation      | Yes     | No       | No       | Wowool aggregates attributes like positions, country, descriptions                                                  |
| Instances        | Yes     | No       | No       | Wowool keeps track of instances, collecting information such as *John Smith, John, He, J. Smith* as the same entity |
| Normalization    | Yes     | No       | No       | In Wowool, *UK* is recognized as the same instance as *United Kingdom*                                              |
| Hyphenation      | Yes     | No       | No       | Stanza does not recognize words that have been split                                                                |
| Augmented        | Yes     | No       | No       | Wowool adds information from Wikipedia to the attributes                                                            |
| Numbers          | Yes     | No       | No       | Resolves written numbers like *five hundred billion dollars*                                                        |
| Sentiment        | Yes     | No       | No       | Wowool returns sentence-based sentiment analysis                                                                    |
| Attributes       | Yes     | No       | No       | Annotations have attributes ex: gender, position, ...                                                               |
| Onthologies      | places  | No       | No       | Things like UK, USA, Belgium, Europe,EU                                                                             |
| Entity types     | +231    | 18       | 18       | The number of different type of entities                                                                            |
| Sub Annotations  | Yes     | No       | No       | Wowool support subannotation like Tripels have Subject, Object, Verb                                                |
| Custom Domains   | Yes     | No       | No       | Does not requires training data, Wowool is a rule-based language                                                    |
| False Positive's |         |          |          |    |
| False Negative's |         |          |          |    |



### Anaphora


`John Dow and Mary Smith went to work at EyeOnText.`

| ?   |   beg |   end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|-----|-------|-------|--------------|---------------|-------------|--------------|--------------|---------------|--------------|---------------|
|     |     0 |     8 | PERSON       | John Dow      | PERSON      | John Dow     | PERSON       | John Dow      | PERSON       | John Dow      |
|     |    13 |    23 | PERSON       | Mary Smith    | PERSON      | Mary Smith   | PERSON       | Mary Smith    | PERSON       | Mary Smith    |
| -   |    40 |    49 | ORG          | EyeOnText     | ORG         | EyeOnText    | ORG          | EyeOnText     | **Missing**  | *EyeOnText*   |



* In the second sentence of the same text, we see that spacy, stanza and google are missing the anaphora references to **Mary Smith** (*she*), **EyeOnText** ( *the it company* ) and **John Dow** (*he*)

`She works for the it company but he only cleans there.`

| ?   |   beg |   end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy       | uri_stanza   | text_stanza      | uri_google   | text_google      |
|-----|-------|-------|--------------|---------------|-------------|------------------|--------------|------------------|--------------|------------------|
| --- |    51 |    54 | PERSON       | Mary Smith    | **Missing** | *She*            | **Missing**  | *She*            | **Missing**  | *She*            |
| --- |    65 |    79 | ORG          | EyeOnText     | **Missing** | *the it company* | **Missing**  | *the it company* | **Missing**  | *the it company* |
| --- |    84 |    86 | PERSON       | John Dow      | **Missing** | *he*             | **Missing**  | *he*             | **Missing**  | *he*             |


#### Wrong tagging

    python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/person_wrong_tagging.txt -a "Sentence,PERSON,ORG,POS,GPE,LOC"

The first instance is correct, but in the second sentence *Georgia* is tagged as a location (**GPE**) 


`Georgia Smith works in Antwerp.`


| beg | end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy    | uri_stanza   | text_stanza   | uri_google   | text_google   |
|-----|-----|--------------|---------------|-------------|---------------|--------------|---------------|--------------|---------------|
|   0 |  13 | PERSON       | Georgia Smith | PERSON      | Georgia Smith | PERSON       | Georgia Smith | PERSON       | Georgia Smith |
|  22 |  29 | GPE          | Antwerp       | GPE         | Antwerp       | GPE          | Antwerp       | GPE          | Antwerp       |


`Georgia is nice, she does a lot.`


| beg | end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|-----|-----|--------------|---------------|-------------|--------------|--------------|---------------|--------------|---------------|
|  31 |  38 | PERSON, LOC  | Georgia Smith | ~~GPE~~     | Georgia      | ~~GPE~~      | Georgia       | ~~GPE~~      | Georgia       |
|  48 |  51 | PERSON       | Georgia Smith | **Missing** | *she*        | **Missing**  | *she*         | **Missing**  | *she*         |


### Conjecture


* spacy and stanza are not tagging the **Position** *CEO*
* google is tagging *CEO* and *Mr.* as a **Person** but they are clearly a Position in this sentence.
* google is then referencing *Miyaktama Mitshu* as being *CEO* while it's the opposite.
* they all miss the anaphora *he*


`The CEO Mr. Miyaktama Mitshu is a bad person he killed a person.`

| beg | end | uri_wowool   | text_wowool      | uri_spacy   | text_spacy       | uri_stanza   | text_stanza      | uri_google   | text_google   |
|-----|-----|--------------|------------------|-------------|------------------|--------------|------------------|--------------|---------------|
|   4 |   7 | POSITION     | CEO              | **Missing** | *CEO*            | **Missing**  | *CEO*            | ~~PERSON~~   | CEO           |
|   8 |  11 |              | *Mr.*            |             | *Mr.*            |              | *Mr.*            | PERSON       | CEO           |
|  12 |  28 | PERSON       | Miyaktama Mitshu | PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu | PERSON       | CEO           |
|  38 |  44 |              | *person*         |             | *person*         |              | *person*         | PERSON       | CEO           |
|  45 |  47 | PERSON       | Miyaktama Mitshu | **Missing** | *he*             | **Missing**  | *he*             | **Missing**  | *he*          |
|  55 |  61 |              | *person*         |             | *person*         |              | *person*         | PERSON       | person        |

* spacy is mistagging *Miyaktama* as a **GPE**, while stanza, google lost the reference to *Miyaktama Mitshu*
* spacy, stanza and google do not reference *the CEO* to *Miyaktama Mitshu*, google just finds the *CEO* as a **PERSON** while it should be a **POSITION**.

`Miyaktama is the CEO.`


| beg | end | uri_wowool   | text_wowool      | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|-----|-----|--------------|------------------|-------------|--------------|--------------|---------------|--------------|---------------|
|  63 |  72 | PERSON       | Miyaktama Mitshu | ~~GPE~~     | Miyaktama    | PERSON       | Miyaktama     | PERSON       | Miyaktama     |
|  76 |  83 | PERSON       | Miyaktama Mitshu | **Missing** | *the CEO*    | **Missing**  | *the CEO*     | **Missing**  | *the CEO*     |
|  80 |  83 | POSITION     | CEO              | **Missing** | *CEO*        | **Missing**  | *CEO*         | ~~PERSON~~   | CEO           |

But it is clear from the first sentence that it is a Person.


### Normalization

While performing NER it is very important to apply text normalization so that you can use the output directly for data science. Wowool is the only engine that does this:

`The question is whether Marion will seek to have a [political] standing of her own.”.`


|   beg |   end | uri_wowool   | text_wowool     | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|-------|-------|--------------|-----------------|-------------|--------------|--------------|---------------|
|  5783 |  5789 | PERSON       | Marion Maréchal | ~~ORG~~     | Marion       | PERSON       | Marion        |
|  5834 |  5837 | PERSON       | Marion Maréchal | **Missing** | *her*        | **Missing**  | *her*         |



### Hyphenation

Testing a text that contains hyphenations. This happens a lot with pdf documents that use columns

    python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/hyphenation.txt

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

* spacy and stanza are not dealing with hyphenations.
* google does, but does not clean it up and does sometimes tag it wrongly: *Rene* is a Person but not in this case. *Renecarel* is a street name. I would even argue that *street* on its own is not a location.


| beg | end | uri_wowool   | URI_wowool   | text_wowool         | uri_spacy   | text_spacy           | uri_stanza   | text_stanza          | uri_google   | URI_google   | text_google          |
|-----|-----|--------------|--------------|---------------------|-------------|----------------------|--------------|----------------------|--------------|--------------|----------------------|
|  15 |  22 | GPE          | City         | Antwerp             | **Missing** | *Ant-\nwerp*         | **Missing**  | *Ant-\nwerp*         | GPE          | LOCATION     | Ant-\nwerp           |
|  32 |  50 | LOC          | Street       | Renecarel street    | **Missing** | *Rene-\ncarel street*| **Missing**  | *Rene-\ncarel street*| **Missing**  |              | *Rene-\ncarel street*|
|  32 |  36 |              |              | *Rene*              | **Missing** | *Rene*               | **Missing**  | *Rene*               | ~~PERSON~~   | ~~PERSON~~   | Rene                 |
|  44 |  50 |              |              | *street*            | **Missing** | *street*             | **Missing**  | *street*             | GPE          | LOCATION     | street               |
|  69 |  86 | FAC          | Facility     | *Rivirenhof Park*   | **Missing** | *Riviren-\nhof Park* | **Missing**  | *Riviren-\nhof Park* | GPE          | LOCATION     | Riviren-\nhof Park   |


#### Spacy.io Demo text

Runnig a text i've found in the demo from Spacy.io.

    python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/companies.txt -a "Sentence,PERSON,FAC,ORG,POSITION,GPE,LOC,PRODUCT,WORK_OF_ART"

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

* stanza is splitting *Sebastian Thrun* into 2 Persons, which is wrong.
* google is tagging *people* as a Person
* spacy,stanza and google are missing *the company*, and google tags *company* as a ORGANIZATION which is wrong.
* spacy,stanza and google are missing *him*

| beg | end | uri_wowool   | URI_wowool   | text_wowool     | uri_spacy   | URI_spacy   | text_spacy      | uri_stanza   | URI_stanza   | text_stanza   | uri_google   | URI_google       | text_google     |
|-----|-----|--------------|--------------|-----------------|-------------|-------------|-----------------|--------------|--------------|---------------|--------------|------------------|-----------------|
|   5 |  20 | PERSON       | Person       | Sebastian Thrun | PERSON      | PERSON      | Sebastian Thrun | PERSON       | PERSON       | Sebastian     | PERSON       | PERSON           | Sebastian Thrun |
|  15 |  20 |              |              | *Thrun*         |             |             | *Thrun*         | PERSON       | PERSON       | Thrun         |              |                  | *Thrun*         |
|  61 |  67 | ORG          | Company      | Google          | ORG         | ORG         | Google          | ORG          | ORG          | Google        | ORG          | ORGANIZATION     | Google          |
|  80 |  86 |              |              | *people*        |             |             | *people*        |              |              | *people*      | ~~PERSON~~   | ~~PERSON~~       | people          |
|  98 | 109 | ORG          | Company      | Google          | **Missing** |             | *the company*   | **Missing**  |              | *the company* | **Missing**  |                  | *the company*   |
| 102 | 109 |              |              | *company*       |             |             | *company*       |              |              | *company*     | ~~ORG~~      | ~~ORGANIZATION~~ | company         |
| 115 | 118 | PERSON       | Person       | Sebastian Thrun | **Missing** |             | *him*           | **Missing**  |              | *him*         | **Missing**  |                  | *him*           |


`"I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn't worth talking to." said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

* wowool is the only one capturing the POSITION
* google is adding a lot of wrong tags like *CEOs* as PERSON or *car companies* as ORGANIZATION
* spacy is wrongly tagging *Thrun* as a GPE, stanza get it correct but looses the refernce to *Sebastian Thrun*, only google and wowool get it correctly.
* spacy is missing the startup *Udacity*
* google are missing *Recode* and stanza thinks it's a WORK_OF_ART
* spacy and stanza are also missing the positions *co-founder* and *CEO* , while google thinks these are PERSON's
 

| beg | end | uri_wowool   | URI_wowool   | text_wowool                | uri_spacy   | URI_spacy   | text_spacy                 | uri_stanza   | URI_stanza      | text_stanza                | uri_google   | URI_google   | text_google     |
|-----|-----|--------------|--------------|----------------------------|-------------|-------------|----------------------------|--------------|-----------------|----------------------------|--------------|--------------|-----------------|
| 151 | 162 | POSITION     | Position     | CEO                        | **Missing** |             | *senior CEOs*              | **Missing**  |                 | *senior CEOs*              | **Missing**  |              | *senior CEOs*   |
| 158 | 162 |              |              | *CEOs*                     |             |             | *CEOs*                     |              |                 | *CEOs*                     | PERSON       | PERSON       | CEOs            |
| 172 | 180 | **Missing**  |              | *American*                 | **Missing** |             | *American*                 | **Missing**  |                 | *American*                 | GPE          | LOCATION     | American        |
| 181 | 194 |              |              | *car companies*            |             |             | *car companies*            |              |                 | *car companies*            | ORG          | ORGANIZATION | car companies   |
| 270 | 275 | PERSON       | Person       | Sebastian Thrun            | GPE         | GPE         | Thrun                      | PERSON       | PERSON          | Thrun                      | PERSON       | PERSON       | Sebastian Thrun |
| 285 | 295 | POSITION     | Position     | co - founder               | **Missing** |             | *co-founder*               | **Missing**  |                 | *co-founder*               | PERSON       | PERSON       | co-founder      |
| 300 | 303 | POSITION     | Position     | CEO                        | **Missing** |             | *CEO*                      | **Missing**  |                 | *CEO*                      | PERSON       | PERSON       | CEO             |
| 314 | 338 |              |              | *higher education startup* |             |             | *higher education startup* |              |                 | *higher education startup* | ORG          | ORGANIZATION | Udacity         |
| 339 | 346 | ORG          | Company      | Udacity                    | **Missing** |             | *Udacity*                  | ORG          | ORG             | Udacity                    | ORG          | ORGANIZATION | Udacity         |
| 369 | 375 | ORG          | Company      | Recode                     | ORG         | ORG         | Recode                     | **Missing**  | ~~WORK_OF_ART~~ | Recode                     | **Missing**  |              | *Recode*        |


As you can see spacy does not look good on their own demo text, imagine on unknown territory.



## Spacy vs Wowool

### Features

#### Speed

We can say that wowool and spacy has a very similair speed

#### Accuracy

Wowool out performs by far Spacy, As SpaCy

#### Features

| Feature          | Wowool  | SpaCy    | Notes                                                                                                               |
|:-----------------|:-------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora         | Yes     | No       | SpaCy does not resolve pronouns like he, she, the city, the company, etc.                                           |
| Conjecture       | Yes     | No       | When Mentioning a something in context, wowool will remeber that what it was later on                               |
| Aggregation      | Yes     | No       | Wowool aggregates attributes like positions, country, descriptions                                                  |
| Instances        | Yes     | No       | Wowool keeps track of instances, collecting information such as *John Smith, John, He, J. Smith* as the same entity |
| Normalization    | Yes     | No       | In Wowool, *UK* is recognized as the same instance as *United Kingdom*                                              |
| Hyphenation      | Yes     | No       | SpaCy does not recognize words that have been split                                                                 |
| Augmented        | Yes     | No       | Wowool adds information from Wikipedia to the attributes                                                            |
| Numbers          | Yes     | No       | Resolves written numbers like *five hundred billion dollars*                                                        |
| Sentiment        | Yes     | No       | Wowool returns sentence-based sentiment analysis                                                                    |
| Attributes       | Yes     | No       | Annotations have attributes ex: gender, position, ...                                                               |
| Onthologies      | places  | No       | Things like UK, USA, Belgium, Europe,EU                                                                             |
| Entity types     | +231    | 18       | The number of different type of entities                                                                            |
| Sub Annotations  | Yes     | No       | Wowool support subannotation like Tripels have Subject, Object, Verb                                                |
| Custom Domains   | Yes     | No       | SpaCy requires training data, while Wowool is a rule-based language                                                 |
| False Positive's |         |          |    |
| False Negative's |         |          |    |


### Comparing

Notes: we used the `en_core_web_sm` to compare with wowool, but we noticed that using other models returns inconsistencies during the tests. As some of their own entities disappear and other appeare in other models, so we decided to stick to this model.


### Setup

    pip install spacy
    python -m spacy download en_core_web_sm


Using this command you will see the comparison between spacy and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e spacy


### Results

#### Anaphora

    python3 -m nlp_compare -e spacy -l english -p "english,entity" -f tests/data/anaphora.text

As we can see spacy is missing all the references in the second sentence  **Mary Smith** (*she*), **EyeOnText** ( *the IT company* )  and **John Dow** (*he*)

`John Dow and Mary Smith went to work at EyeOnText.`

|   beg |   end | uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------|------------------|-------------------|
|     0 |     8 | PERSON    | John Dow   | PERSON           | John Dow          |
|    13 |    23 | PERSON    | Mary Smith | PERSON           | Mary Smith        |
|    40 |    49 | ORG       | EyeOnText  | ORG              | EyeOnText         |


`She works for the IT company but he only cleans there.`

|   beg |   end | uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------|------------------|-------------------|
|    51 |    54 | PERSON    | Mary Smith | **Missing**      |                   |
|    65 |    79 | ORG       | EyeOnText  | **Missing**      |                   |
|    84 |    86 | PERSON    | John Dow   | **Missing**      |                   |


#### Wrong tagging

As we can see spacy is incorrectly tagging **the George Washington** missing **John Smith** and missing the location **Washington** from **longtime Washington lawyer**

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

The first instance is correct, but in the second sentence **Georgia** is tagged as a location (**GPE**) 

`Georgia Smith work in Antwerp.`

|   beg |   end | uri_wow     | text_wow      | uri_spacy   | text_spacy    |
|-------|-------|-------------|---------------|-------------|---------------|
|     0 |    13 | PERSON      | Georgia Smith | PERSON      | Georgia Smith |
|    22 |    31 | **Missing** |               | GPE         | Antwerpen     |


`Georgia is nice, she does a lot.`

|   beg |   end | uri_wow   | text_wow      | uri_spacy   | text_spacy   |
|-------|-------|-----------|---------------|-------------|--------------|
|    33 |    40 | PERSON    | Georgia Smith | GPE         | Georgia      |
|    33 |    40 | LOC       | Georgia       | **Missing** |              |
|    50 |    53 | PERSON    | Georgia Smith | **Missing** |              |

#### Conjecture

As we can see spacy is incorrectly tagging **Miyaktama** in the second sentence as an organization, although it is clear from the first sentence that it is a Person.

`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------------|------------------|-------------------|
|     4 |    20 | PERSON    | Miyaktama Mitshu | PERSON           | Miyaktama Mitshu  |

`Miyaktama is a very good leader.`

|   beg |   end | uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-------|-------|-----------|------------------|------------------|-------------------|
|    50 |    59 | PERSON    | Miyaktama Mitshu | ORG              | Miyaktama         |

#### Spacy demo sample data

We are testing the sample sentences in the site of Displacy

In this first sentence, the references to **the company** and **him** are lost in spacy.

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

|   beg |   end | uri_wow   | text_wow        | uri_spacy        | text_spacy        |
|-------|-------|-----------|-----------------|------------------|-------------------|
|     5 |    20 | PERSON    | Sebastian Thrun | PERSON           | Sebastian Thrun   |
|    61 |    67 | ORG       | Google          | ORG              | Google            |
|    71 |    75 | CARDINAL  | 2007            | DATE             | 2007              |
|    98 |   109 | ORG       | Google          | **Missing**      |                   |
|   115 |   118 | PERSON    | Sebastian Thrun | **Missing**      |                   |


The reference to **Thrun**, who is mentioned in the previous sentence, is lost and the name is wrongly identified as a location. Spacy is also missing **Udacity** as a company, whereas it is clearly identified as a startup.

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

|   beg |   end | uri_wow     | text_wow        | uri_spacy        | text_spacy        |
|-------|-------|-------------|-----------------|------------------|-------------------|
|   270 |   275 | PERSON      | Sebastian Thrun | GPE              | Thrun             |
|   339 |   346 | ORG         | Udacity         | **Missing**      |                   |
|   369 |   375 | ORG         | Recode          | ORG              | Recode            |
|   376 |   393 | **Missing** |                 | DATE             | earlier this week |

#### Hyphenation

    python3 -m nlp_compare -e spacy -l english -p "english,entity" -f tests/data/hyphenation.txt

As we see, none of these entities are found. Note that this happens a lot with PDF documents that use colums.

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

|   beg |   end | uri_wow   | text_wow         | uri_spacy   | text_spacy   |
|-------|-------|-----------|------------------|-------------|--------------|
|    15 |    22 | GPE       | Antwerp          | **Missing** |              |
|    32 |    50 | LOC       | Renecarel street | **Missing** |              |
|    69 |    86 | LOC       | Rivirenhof Park  | **Missing** |              |

#### Tokenization

Tokenization seems to be a bit random in the case of alphanumeric characters. Note for example **A66** vs **A1M**.

`A66 in County Durham/Cumbria closed in both directions between A1M (J53) and M6 (J40) - snow .`

Tokens:

```
A66
in
County
Durham
/
Cumbria
closed
in
both
directions
between
A1
M
(
J53
)
and
M6
(
J40
)
-
snow
.
```

Entities are also off:

```
A66 - ORG
County Durham/Cumbria - ORG
A1M - PERSON
M6 (J40 - ORG
```


## Stanza vs Wowool

### Setup

    pip install stanza


### Features

#### Speed

We wowool is up to 50 to 100 faster, and wowool is only using 1 cpu while stanza is using all off them, going up to 800% CPU usage.

#### Accuracy

Wowool out performs by far Stanza

#### Features

| Feature          | Wowool  | Stanza   | Notes                                                                                                               |
|:-----------------|:-------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora         | Yes     | No       | Stanza does not resolve pronouns like he, she, the city, the company, etc.                                          |
| Conjecture       | Yes     | No       | When Mentioning a something in context, wowool will remeber that what it was later on                               |
| Aggregation      | Yes     | No       | Wowool aggregates attributes like positions, country, descriptions                                                  |
| Instances        | Yes     | No       | Wowool keeps track of instances, collecting information such as *John Smith, John, He, J. Smith* as the same entity |
| Normalization    | Yes     | No       | In Wowool, *UK* is recognized as the same instance as *United Kingdom*                                              |
| Hyphenation      | Yes     | No       | Stanza does not recognize words that have been split                                                                |
| Augmented        | Yes     | No       | Wowool adds information from Wikipedia to the attributes                                                            |
| Numbers          | Yes     | No       | Resolves written numbers like *five hundred billion dollars*                                                        |
| Sentiment        | Yes     | No       | Wowool returns sentence-based sentiment analysis                                                                    |
| Attributes       | Yes     | No       | Annotations have attributes ex: gender, position, ...                                                               |
| Onthologies      | places  | No       | Things like UK, USA, Belgium, Europe,EU                                                                             |
| Entity types     | +231    | 18       | The number of different type of entities                                                                            |
| Sub Annotations  | Yes     | No       | Wowool support subannotation like Tripels have Subject, Object, Verb                                                |
| Custom Domains   | Yes     | No       | Stanza requires training data, while Wowool is a rule-based language                                                |
| False Positive's |         |          |    |
| False Negative's |         |          |    |

### Comparing

Using this command you will see the comparison between stanza and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e stanza --show

#### Anaphora

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/anaphora.txt

First, some speed results:

* Wowool startup time: 0.247
* Stanza startup time: 8.582
* Processing time of stanza: 0.701 Counter({'PERSON': 2, 'ORG': 1})
* Processing time of wowool: 0.010 Counter({'PERSON': 4, 'ORG': 2})
* Wowool is 73.213 times faster than stanza

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

As we can see spacy is incorrectly tagging **George Washington** as a location, missing **John Smith**, and missing the location **Washington** from **longtime Washington lawyer**.

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

The first instance is correct, but in the second sentence **Georgia** is tagged as a location (**GPE**).

`Georgia Smith work in Antwerpen.`

|   beg |   end | uri_wow     | text_wow      | uri_stanza   | text_stanza   |
|-------|-------|-------------|---------------|--------------|---------------|
|     0 |    13 | PERSON      | Georgia Smith | PERSON       | Georgia Smith |
|    22 |    31 | **Missing** |               | GPE          | Antwerpen     |

`Georgia is nice, she does a lot.`

|   beg |   end | uri_wow   | text_wow      | uri_stanza   | text_stanza   |
|-------|-------|-----------|---------------|--------------|---------------|
|    33 |    40 | PERSON    | Georgia Smith | GPE          | Georgia       |
|    33 |    40 | LOC       | Georgia       | **Missing**  |               |
|    50 |    53 | PERSON    | Georgia Smith | **Missing**  |               |

#### Conjecture

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/person_conjecture.txt

Stanza is doing better than spacy in this case, but still loses the reference to **Miyaktama Mitshu**.

`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza      |
|-------|-------|-----------|------------------|--------------|------------------|
|     4 |    20 | PERSON    | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu |


`Miyaktama is a very good leader.`

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza   |
|-------|-------|-----------|------------------|--------------|---------------|
|    50 |    59 | PERSON    | Miyaktama Mitshu | PERSON       | Miyaktama     |

#### Spacy demo sample data.

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/companies.txt

In this case stanza split the name **Sebastian Thrun** in two Persons, where it is just one. They are missing **Google** as *the company* and **Sebastian Thrun** as *him* 

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

Here they do capture **Udacity** but are wrongly assinging **Recode** as a **WORK_OF_ART**

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

|   beg |   end | uri_wow     | text_wow        | uri_stanza   | text_stanza       |
|-------|-------|-------------|-----------------|--------------|-------------------|
|   270 |   275 | PERSON      | Sebastian Thrun | PERSON       | Thrun             |
|   339 |   346 | ORG         | Udacity         | ORG          | Udacity           |
|   369 |   375 | ORG         | Recode          | WORK_OF_ART  | Recode            |


#### Hyphenation

    python3 -m nlp_compare -e stanza -l english -p "english,entity" -f tests/data/hyphenation.txt

Stanza does find these entities, but the literal has not been resoved.

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza        |
|-------|-------|-----------|------------------|--------------|--------------------|
|    15 |    22 | GPE       | Antwerp          | **Missing**  |                    |
|    32 |    50 | LOC       | Renecarel street | FAC          | Rene-\ncarel street |
|    69 |    86 | LOC       | Rivirenhof Park  | FAC          | Riviren-\nhof Park  |

## Google vs Wowool

First of, there seems to be a bug in GoogleAPI. If an entity is on offset 0 then the REST API does not return an offset in the mentioned object. You can add a space in front of your text, but then all your offsets are off, or you need to add a hack into your code.

#### Anaphora

    python3 -m nlp_compare -e google -l english -p "english,entity" -f tests/data/anaphora.txt

`John Dow and Mary Smith went to work at EyeOnText.`

|   beg |   end | uri_wow      | text_wow   | uri_google   | text_google   |
|-------|-------|--------------|------------|--------------|---------------|
|     0 |     8 | PERSON       | John Dow   | PERSON       | John Dow      |
|    13 |    23 | PERSON       | Mary Smith | PERSON       | Mary Smith    |
|    40 |    49 | ORGANIZATION | EyeOnText  | OTHER        | EyeOnText     |


`She works for the it company but he only cleans there.`

|   beg |   end | uri_wow      | text_wow   | uri_google   | text_google   |
|-------|-------|--------------|------------|--------------|---------------|
|    51 |    54 | PERSON       | Mary Smith | **Missing**  |               |
|    65 |    79 | ORGANIZATION | EyeOnText  | **Missing**  |               |
|    69 |    79 | **Missing**  |            | ORGANIZATION | it company    |
|    84 |    86 | PERSON       | John Dow   | **Missing**  |               |

Total:  Time: google  : 0.303 Counter({'PERSON': 2, 'OTHER': 1, 'ORGANIZATION': 1})
Total:  Time: Wowool  : 0.009 Counter({'PERSON': 4, 'ORGANIZATION': 2})

#### Wrong tagging

    python3 -m nlp_compare -e google -l english -p "english,entity" -f tests/data/person_wrong_names.txt

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

|   beg |   end | uri_wow     | text_wow      | uri_google   | text_google       |
|-------|-------|-------------|---------------|--------------|-------------------|
|     0 |    10 | PERSON      | John Smith    | PERSON       | John Smith        |
|    16 |    33 | **Missing** |               | PERSON       | George Washington |
|    23 |    33 | LOCATION    | Washington    | **Missing**  |                   |
|    34 |    47 | **Missing** |               | ~~PERSON~~   | law professor     |
|    38 |    47 | Position    | professor     | **Missing**  |                   |
|    52 |    65 | PERSON      | Eugene Fidell | PERSON       | Eugene Fidell     |
|    78 |    88 | LOCATION    | Washington    | LOCATION     | Washington        |
|    78 |    88 | GPE         | Washington    | **Missing**  |                   |
|    89 |    95 | Position    | lawyer        | ~~PERSON~~       | lawyer            |


`He worked with the president George Washington.`

|   beg |   end | uri_wow   | text_wow          | uri_google   | text_google       |
|-------|-------|-----------|-------------------|--------------|-------------------|
|    97 |    99 | PERSON    | John Smith        | **Missing**  |                   |
|   116 |   125 | Position  | president         | ~~PERSON~~   | president         |
|   126 |   143 | PERSON    | George Washington | PERSON       | George Washington |
|   133 |   143 | LOCATION  | Washington        | **Missing**  |                   |

Total:  Time: google  : 0.306 Counter({'PERSON': 7, 'LOCATION': 1})
Total:  Time: Wowool  : 0.017 Counter({'PERSON': 4, 'LOCATION': 3, 'Position': 3, 'GPE': 1})

#### Conjecture


    python3 -m nlp_compare -e google -l english -p "english,entity" -f tests/data/person_conjecture.txt

`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow     | text_wow         | uri_google   | text_google      |
|-------|-------|-------------|------------------|--------------|------------------|
|     0 |     3 | **Missing** |                  | ~~PERSON~~   | Mr.              |
|     4 |    20 | PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu |
|    42 |    48 | **Missing** |                  | PERSON       | person           |


`Miyaktama is a very good leader.`

|   beg |   end | uri_wow     | text_wow         | uri_google   | text_google   |
|-------|-------|-------------|------------------|--------------|---------------|
|    50 |    59 | PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama     |
|    75 |    81 | **Missing** |                  | ~~PERSON~~       | leader        |

Total:  Time: google  : 0.815 Counter({'PERSON': 5})
Total:  Time: Wowool  : 0.007 Counter({'PERSON': 2})

#### Spacy demo sample data.

    python3 -m nlp_compare -e google -l english -p "english,entity" -f tests/data/companies.txt

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

|   beg |   end | uri_wow      | text_wow        | uri_google   | text_google       |
|-------|-------|--------------|-----------------|--------------|-------------------|
|     5 |    20 | PERSON       | Sebastian Thrun | PERSON       | Sebastian Thrun   |
|    40 |    57 | **Missing**  |                 | OTHER        | self-driving cars |
|    61 |    67 | ORGANIZATION | Google          | ORGANIZATION | Google            |
|    71 |    75 | **Missing**  |                 | DATE         | 2007              |
|    71 |    75 | CARDINAL     | 2007            | NUMBER       | 2007              |
|    80 |    86 | **Missing**  |                 | ~~PERSON~~   | people            |
|    98 |   109 | ORGANIZATION | Google          | **Missing**  |                   |
|   102 |   109 | **Missing**  |                 | ORGANIZATION | company           |
|   115 |   118 | PERSON       | Sebastian Thrun | **Missing**  |                   |


`“I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn't worth talking to.`

|   beg |   end | uri_wow     | text_wow   | uri_google   | text_google   |
|-------|-------|-------------|------------|--------------|---------------|
|   151 |   162 | Position    | CEO        | **Missing**  |               |
|   160 |   164 | **Missing** |            | PERSON       | CEOs          |
|   172 |   180 | NORP        | American   | **Missing**  |               |
|   174 |   182 | **Missing** |            | ~~LOCATION~~     | American      |
|   183 |   196 | **Missing** |            | ~~ORGANIZATION~~ | car companies |
|   212 |   216 | **Missing** |            | OTHER        | hand          |


`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

|   beg |   end | uri_wow      | text_wow        | uri_google   | text_google              |
|-------|-------|--------------|-----------------|--------------|--------------------------|
|   270 |   275 | PERSON       | Sebastian Thrun | **Missing**  |                          |
|   272 |   277 | **Missing**  |                 | ~~PERSON~~     | Thrun                    |
|   285 |   295 | Position     | co - founder    | **Missing**  |                          |
|   287 |   297 | **Missing**  |                 | ~~PERSON~~     | co-founder               |
|   300 |   303 | Position     | CEO             | **Missing**  |                          |
|   302 |   305 | **Missing**  |                 | ~~PERSON~~     | CEO                      |
|   316 |   340 | **Missing**  |                 | ORGANIZATION | higher education startup |
|   339 |   346 | ORGANIZATION | Udacity         | ORGANIZATION | Udacity                  |
|   369 |   375 | ORGANIZATION | Recode          | **Missing**  |                          |
|   371 |   375 | **Missing**  |                 | OTHER        | Recode                   |

Total:  Time: google  : 0.759 Counter({'PERSON': 6, 'ORGANIZATION': 5, 'OTHER': 3, 'LOCATION': 1, 'EVENT': 1, 'DATE': 1, 'NUMBER': 1})
Total:  Time: Wowool  : 0.025 Counter({'ORGANIZATION': 4, 'PERSON': 3, 'Position': 3, 'NORP': 1})

#### Hyphenation

    python3 -m nlp_compare -e google -l english -p "english,entity" -f tests/data/hyphenation.txt

Google does find these entities, but the literal has not been resolved and they are confused with the street. **Renecarel street** as they find **Rene** and **street**

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

|   beg |   end | uri_wow     | text_wow         | uri_google   | text_google       |
|-------|-------|-------------|------------------|--------------|-------------------|
|    15 |    24 | GPE         | Antwerp                 | LOCATION     | Ant-\nwerp |
|    32 |    50 | LOCATION    | Renecarel street | **Missing**  |                   |
|    32 |    36 | **Missing** |                  | ~~PERSON~~   | Rene              |
|    44 |    50 | **Missing** |                  | LOCATION     | street            |
|    69 |    86 | LOCATION    | Rivirenhof Park  | LOCATION     | Riviren-\nhof Park|


## Findings

In this project, we compared various Natural Language Processing (NLP) engines to evaluate their performance on name entity recognition (NER). The key findings are as follow:

### Restricting our entity space

To make the comparison as fair as possible we had to restrict our entity space and remove the attribute information that is part of the entity annotations like (sector, gender, position, headquarters, key_people and more). This was necessary because the compared engines simply did not produce as rich an information output as we do.

### Speed

* Wowool has similar speed as Spacy but returns much richer information, even with the applied restrictions
* Wowool has a much faster startup time. Especially compared to Stanza, which is very slow both in startup and processing speed (up to 100x)

### Accuracy

It is very clear that Wowool knows about language and tackles all the linguistic issues that machine learning engines cannot tackle like anaphora, conjecture, hyphenation, instances, name references and more. 

* Wowool: **PERSON**: 3250, **ORG**: 2836,
* Spacy: **PERSON**: 1652, **ORG**: 2357,
* Stanza: **PERSON**: 1716, **ORG**: 1479,

WOWOOL: Counter({'Person.': 3278, 'PersonMention': 2278, 'Event': 1909, 'Publisher': 1094, 'Company': 1049, 'Position': 995, 'Organization': 694, 'Country': 683, 'Facility': 542, 'PlaceAdj': 522, 'Date': 421, 'City': 359, 'Url': 328, 'WorldRegion': 275, 'They': 208, 'Month': 195, 'MoneyAmount': 95, 'CurrencyUnit': 24, 'Email': 12, 'Street': 9})
Spacy: Counter({'ORG': 2357, 'PERSON': 1652, 'DATE': 1155, 'GPE': 1065, 'CARDINAL': 890, 'NORP': 344, 'LANGUAGE': 322, 'ORDINAL': 149, 'TIME': 128, 'WORK_OF_ART': 101, 'MONEY': 95, 'LOC': 75, 'PERCENT': 75, 'FAC': 38, 'PRODUCT': 34, 'QUANTITY': 23, 'EVENT': 11, 'LAW': 4})
Stanza: Counter({'PERSON': 1716, 'ORG': 1479, 'DATE': 1114, 'GPE': 1006, 'CARDINAL': 579, 'NORP': 369, 'LANGUAGE': 323, 'WORK_OF_ART': 261, 'ORDINAL': 155, 'TIME': 120, 'MONEY': 104, 'EVENT': 98, 'PERCENT': 79, 'LOC': 77, 'FAC': 59, 'PRODUCT': 32, 'QUANTITY': 29, 'LAW': 15})

|     URI     | Wowool | Spacy | Stanza
|-------------|--------|-------|-------|
| PERSON      | 3278   | 1652  | 1716  |
| ORG         |  see Company,Organization    | 2357  |  1479  |
| Company     | 1049 | | |
| Organization| 694  | | |





Note: we need to add false positive stats  here.

### Resource Utilization

First, size on disk:

|  name  |      model     | size in Mb |  Max text     |
|--------|----------------|:----------:|---------------|
| wowool | english-entity | 14         |               |
| spacy  | n_core_web_sm  | 15         | <1Mb          |
| stanza | en             | 1100       |               |

Second, consumed memory:

* Wowool uses 600M to process 1M
* Spacy scales very poorly, giving us the following message `Text of length 1132067 exceeds maximum of 1000000. The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input.`
* Stanza uses a max of 2G

In short, spacy does not handle big data, and stanza looks like it does handle bigger data sets but it takes an incredibly long time (718 sec) to process a 1 Mb file, and it uses 11 threads during the process. In contrast, Wowool processed the same input using a single thread in 24 seconds.

### Things that go wrong in unexplainable ways

`Most nonprofits, experts say, don't or can't provide third-party data about the costs and benefits of their interventions.`


|   beg |   end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|-------|-------|--------------|---------------|-------------|--------------|--------------|---------------|
|  4729 |  4732 | **Missing**  | *n’t*         | GPE         | n’t          | **Missing**  | *n’t*         |


`The final chapter is, perhaps inevitably, called What to Whole-Arse.`


|   beg |   end | uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|-------|-------|--------------|---------------|-------------|--------------|--------------|---------------|
|  7787 |  7797 | **Missing**  | *Whole-Arse*  | PERSON      | Whole-Arse   | **Missing**  | *Whole-Arse*  |


* Date's are random in spacy and stanza

╰─❯ python run_spacy.py -m "en_core_web_sm" -i " I read 1363 books."
1363 - CARDINAL
╰─❯ python run_spacy.py -m "en_core_web_sm" -i " I read 1364 books."
1364 - DATE
╰─❯ python run_spacy.py -m "en_core_web_sm" -i " I read 2000 books."
2000 - CARDINAL
╰─❯ python run_spacy.py -m "en_core_web_sm" -i " I read 2001 books."
2001 - DATE
╰─❯ python run_spacy.py -m "en_core_web_sm" -i " I read 2025 books."
2025 - DATE
