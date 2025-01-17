# NLP compare

This tool allows us to compare different nlp engines with the Wowool engine.

## Setup

    pip install -r Wowool-requirements.txt


## Wowool vs Spacy,Stanza and Google

We are going to compare several cases using Wowool, Spacy, Stanza and Google NLP.

| Feature           | Wowool  | Spacy    | Stanza   | Google   | Notes                                                                                                               |
|:------------------|:-------:|:--------:|:--------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora          | Yes     | No       | No       | Poorly   | Most does not resolve pronouns like he, she. only Google resolves some like the city, the company                   |
| Conjecture        | Yes     | No       | No       | No       | When Mentioning a something in context, wowool will remeber that what it was later on                               |
| Custom extraction | Yes     | No       | No       | No       | When Mentioning a something in context, wowool will remeber that what it was later on                               |
| Aggregation       | Yes     | No       | No       | No       | Wowool aggregates attributes like positions, country, descriptions                                                  |
| Instances         | Yes     | No       | No       | No       | Wowool keeps track of instances, collecting information such as *John Smith, John, He, J. Smith* as the same entity |
| Normalization     | Yes     | No       | No       | Yes      | In Wowool, *UK* is recognized as the same instance as *United Kingdom*                                              |
| Hyphenation       | Yes     | No       | No       | Poorly   | Stanza does not recognize words that have been split,google does not cleanup, and get it wrong with partial matches |
| Augmented         | Yes     | No       | No       | Link     | Wowool adds information to the entity that can be used (key people,headqurters,positions), Google only the link to Wikipedia |
| Numbers           | Yes     | No       | No       | Yes      | Resolves written numbers like *five hundred billion dollars* -> 500000000700, *$2bn* -> 2000000000                  |
| Resolving Dates   | Yes     | No       | No       | No       | Resolving to absolute dates. like: *two year ago* to the actual date starting from the initial publishing date      | 
| Sentiment         | Yes     | Yes      | No       | Yes      | Wowool returns sentence-based sentiment analysis vs document bases.                                                 |
| Attributes        | Yes     | No       | No       | No       | Annotations have attributes ex: gender, position, ...                                                               |
| Onthologies       | places  | No       | No       | No       | Things like UK, USA, Belgium, Europe,EU                                                                             |
| Entity types      | +231    | 18       | 18       | 18       | The number of different type of entities                                                                            |
| Sub Annotations   | Yes     | No       | No       | No       | Wowool support subannotation like Tripels have Subject, Object, Verb                                                |
| Custom Domains    | Yes     | No       | No       | No       | Does not requires training data, Wowool is a rule-based language                                                    |
| False Positive's  |         |          |          |          |    |
| False Negative's  |         |          |          |          |    |


### Anaphora

None of the NLP engines except Wowool is resolving the Anaphora.
In the second sentence of the same text, we see that Spacy, Stanza and Google are missing the anaphora references to:

* *Mary Smith (she)*, 
* *EyeOnText (the IT company)*
* *John Doe (he)*

`John Doe and Mary Smith went to work at EyeOnText.`

| uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|--------------|---------------|-------------|--------------|--------------|---------------|--------------|---------------|
| PERSON       | John Doe      | PERSON      | John Doe     | PERSON       | John Doe      | PERSON       | John Doe      |
| PERSON       | Mary Smith    | PERSON      | Mary Smith   | PERSON       | Mary Smith    | PERSON       | Mary Smith    |
| ORG          | EyeOnText     | ORG         | EyeOnText    | ORG          | EyeOnText     | **Missing**  | *EyeOnText*   |


`She works for the IT company but he only cleans there.`

| uri_wowool   | text_wowool   | uri_spacy   | text_spacy       | uri_stanza   | text_stanza      | uri_google   | text_google      |
|--------------|---------------|-------------|------------------|--------------|------------------|--------------|------------------|
| PERSON       | Mary Smith    | **Missing** | *She*            | **Missing**  | *She*            | **Missing**  | *She*            |
| ORG          | EyeOnText     | **Missing** | *the IT company* | **Missing**  | *the IT company* | **Missing**  | *the IT company* |
| PERSON       | John Doe      | **Missing** | *he*             | **Missing**  | *he*             | **Missing**  | *he*             |


### Wrong tagging


The first instance is correct, but in the second sentence *Georgia* is tagged as a location (**GPE**) 


`Georgia Smith works in Antwerp.`


| uri_wowool   | text_wowool   | uri_spacy   | text_spacy    | uri_stanza   | text_stanza   | uri_google   | text_google   |
|--------------|---------------|-------------|---------------|--------------|---------------|--------------|---------------|
| PERSON       | Georgia Smith | PERSON      | Georgia Smith | PERSON       | Georgia Smith | PERSON       | Georgia Smith |
| GPE          | Antwerp       | GPE         | Antwerp       | GPE          | Antwerp       | GPE          | Antwerp       |


`Georgia is nice, she does a lot.`


| uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|--------------|---------------|-------------|--------------|--------------|---------------|--------------|---------------|
| PERSON       | Georgia Smith | ~~GPE~~     | Georgia      | ~~GPE~~      | Georgia       | ~~GPE~~      | Georgia       |
| PERSON       | Georgia Smith | **Missing** | *she*        | **Missing**  | *she*         | **Missing**  | *she*         |

***Test:***  python3 -m nlp_compare -e Spacy,stanza,google -l english -p "english,entity" -f tests/data/person_wrong_tagging.txt -a "Sentence,PERSON,ORG,POS,GPE,LOC"


### Conjecture

* Spacy and Stanza are not tagging the **Position** *CEO*
* Google is tagging *CEO* and *Mr.* as a **Person** but they are clearly a Position in this sentence.
* Google is then referencing *Miyaktama Mitshu* as being *CEO* while it's the opposite.
* they all miss the anaphora *he*


`The CEO Mr. Miyaktama Mitshu is a bad person he killed a person.`

| uri_wowool   | text_wowool      | uri_spacy   | text_spacy       | uri_stanza   | text_stanza      | uri_google   | text_google   |
|--------------|------------------|-------------|------------------|--------------|------------------|--------------|---------------|
| POSITION     | CEO              | **Missing** | *CEO*            | **Missing**  | *CEO*            | ~~PERSON~~   | CEO           |
|              | *Mr.*            |             | *Mr.*            |              | *Mr.*            | PERSON       | CEO           |
| PERSON       | Miyaktama Mitshu | PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu | PERSON       | CEO           |
|              | *person*         |             | *person*         |              | *person*         | PERSON       | CEO           |
| PERSON       | Miyaktama Mitshu | **Missing** | *he*             | **Missing**  | *he*             | **Missing**  | *he*          |
|              | *person*         |             | *person*         |              | *person*         | PERSON       | person        |

* Spacy is mistagging *Miyaktama* as a **GPE**, while Stanza and Google lost the reference to *Miyaktama Mitshu*
* Spacy, Stanza and Google do not reference *the CEO* to *Miyaktama Mitshu*, Google just finds the *CEO* as a **PERSON** while it should be a **POSITION**.

`Miyaktama is the CEO.`


| uri_wowool   | text_wowool      | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   | uri_google   | text_google   |
|--------------|------------------|-------------|--------------|--------------|---------------|--------------|---------------|
| PERSON       | Miyaktama Mitshu | ~~GPE~~     | Miyaktama    | PERSON       | Miyaktama     | PERSON       | Miyaktama     |
| PERSON       | Miyaktama Mitshu | **Missing** | *the CEO*    | **Missing**  | *the CEO*     | **Missing**  | *the CEO*     |
| POSITION     | CEO              | **Missing** | *CEO*        | **Missing**  | *CEO*         | ~~PERSON~~   | CEO           |

But it is clear from the first sentence that it is a Person.


### Normalization

While performing NER it is very important to apply text normalization so that you can use the output directly for data science. Wowool is the only engine that does this:

`The question is whether Marion will seek to have a [political] standing of her own.”.`


| uri_wowool   | text_wowool     | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|--------------|-----------------|-------------|--------------|--------------|---------------|
| PERSON       | Marion Maréchal | ~~ORG~~     | Marion       | PERSON       | Marion        |
| PERSON       | Marion Maréchal | **Missing** | *her*        | **Missing**  | *her*         |



### Hyphenation

Testing a text that contains hyphenations. This happens a lot with pdf documents that use columns

    python3 -m nlp_compare -e Spacy,stanza,google -l english -p "english,entity" -f tests/data/hyphenation.txt

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

* Spacy and Stanza are not dealing with hyphenations.
* Google does, but does not clean it up and does sometimes tag it wrongly: *Rene* is a Person but not in this case. *Renecarel* is a street name. I would even argue that *street* on its own is not a location.

| uri_wowool   | URI_wowool   | text_wowool         | uri_spacy   | text_spacy           | uri_stanza   | text_stanza          | uri_google   | URI_google   | text_google          |
|--------------|--------------|---------------------|-------------|----------------------|--------------|----------------------|--------------|--------------|----------------------|
| GPE          | City         | Antwerp             | **Missing** | *Ant-\nwerp*         | **Missing**  | *Ant-\nwerp*         | GPE          | LOCATION     | Ant-\nwerp           |
| LOC          | Street       | Renecarel street    | **Missing** | *Rene-\ncarel street*| **Missing**  | *Rene-\ncarel street*| **Missing**  |              | *Rene-\ncarel street*|
|              |              | *Rene*              | **Missing** | *Rene*               | **Missing**  | *Rene*               | ~~PERSON~~   | ~~PERSON~~   | Rene                 |
|              |              | *street*            | **Missing** | *street*             | **Missing**  | *street*             | GPE          | LOCATION     | street               |
| FAC          | Facility     | *Rivirenhof Park*   | **Missing** | *Riviren-\nhof Park* | **Missing**  | *Riviren-\nhof Park* | GPE          | LOCATION     | Riviren-\nhof Park   |


#### Spacy.io Demo text

Runnig a text found in the demo from Spacy.io.

    python3 -m nlp_compare -e Spacy,stanza,google -l english -p "english,entity" -f tests/data/companies.txt -a "Sentence,PERSON,FAC,ORG,POSITION,GPE,LOC,PRODUCT,WORK_OF_ART"

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

* Stanza is splitting *Sebastian Thrun* into 2 Persons, which is wrong.
* Google is tagging *people* as a Person
* Spacy,stanza and Google are missing *the company*, and Google tags *company* as a ORGANIZATION which is wrong.
* Spacy,stanza and Google are missing *him*

| uri_wowool   | URI_wowool   | text_wowool     | uri_spacy   | URI_spacy   | text_spacy      | uri_stanza   | URI_stanza   | text_stanza   | uri_google   | URI_google       | text_google     |
|--------------|--------------|-----------------|-------------|-------------|-----------------|--------------|--------------|---------------|--------------|------------------|-----------------|
| PERSON       | Person       | Sebastian Thrun | PERSON      | PERSON      | Sebastian Thrun | PERSON       | PERSON       | Sebastian     | PERSON       | PERSON           | Sebastian Thrun |
|              |              | *Thrun*         |             |             | *Thrun*         | PERSON       | PERSON       | Thrun         |              |                  | *Thrun*         |
| ORG          | Company      | Google          | ORG         | ORG         | Google          | ORG          | ORG          | Google        | ORG          | ORGANIZATION     | Google          |
|              |              | *people*        |             |             | *people*        |              |              | *people*      | ~~PERSON~~   | ~~PERSON~~       | people          |
| ORG          | Company      | Google          | **Missing** |             | *the company*   | **Missing**  |              | *the company* | **Missing**  |                  | *the company*   |
|              |              | *company*       |             |             | *company*       |              |              | *company*     | ~~ORG~~      | ~~ORGANIZATION~~ | company         |
| PERSON       | Person       | Sebastian Thrun | **Missing** |             | *him*           | **Missing**  |              | *him*         | **Missing**  |                  | *him*           |


`"I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn't worth talking to." said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

* Wowool is the only one capturing the POSITION
* Google is adding a lot of wrong tags like *CEOs* as PERSON or *car companies* as ORGANIZATION
* Spacy is wrongly tagging *Thrun* as a GPE, Stanza get it correct but looses the refernce to *Sebastian Thrun*, only Google and Wowool get it correctly.
* Spacy is missing the startup *Udacity*
* Google are missing *Recode* and Stanza thinks it's a WORK_OF_ART
* Spacy and Stanza are also missing the positions *co-founder* and *CEO* , while Google thinks these are PERSON's
 
| uri_wowool   | URI_wowool   | text_wowool                | uri_spacy   | URI_spacy   | text_spacy                 | uri_stanza   | URI_stanza      | text_stanza                | uri_google   | URI_google   | text_google     |
|--------------|--------------|----------------------------|-------------|-------------|----------------------------|--------------|-----------------|----------------------------|--------------|--------------|-----------------|
| POSITION     | Position     | CEO                        | **Missing** |             | *senior CEOs*              | **Missing**  |                 | *senior CEOs*              | **Missing**  |              | *senior CEOs*   |
|              |              | *CEOs*                     |             |             | *CEOs*                     |              |                 | *CEOs*                     | PERSON       | PERSON       | CEOs            |
| **Missing**  |              | *American*                 | **Missing** |             | *American*                 | **Missing**  |                 | *American*                 | GPE          | LOCATION     | American        |
|              |              | *car companies*            |             |             | *car companies*            |              |                 | *car companies*            | ORG          | ORGANIZATION | car companies   |
| PERSON       | Person       | Sebastian Thrun            | GPE         | GPE         | Thrun                      | PERSON       | PERSON          | Thrun                      | PERSON       | PERSON       | Sebastian Thrun |
| POSITION     | Position     | co - founder               | **Missing** |             | *co-founder*               | **Missing**  |                 | *co-founder*               | PERSON       | PERSON       | co-founder      |
| POSITION     | Position     | CEO                        | **Missing** |             | *CEO*                      | **Missing**  |                 | *CEO*                      | PERSON       | PERSON       | CEO             |
|              |              | *higher education startup* |             |             | *higher education startup* |              |                 | *higher education startup* | ORG          | ORGANIZATION | Udacity         |
| ORG          | Company      | Udacity                    | **Missing** |             | *Udacity*                  | ORG          | ORG             | Udacity                    | ORG          | ORGANIZATION | Udacity         |
| ORG          | Company      | Recode                     | ORG         | ORG         | Recode                     | **Missing**  | ~~WORK_OF_ART~~ | Recode                     | **Missing**  |              | *Recode*        |


As you can see Spacy does not look good on their own demo text, imagine on unknown territory.



## Spacy vs Wowool

### Features

#### Speed

We can say that Wowool and Spacy has a very similair speed, if we reduce our entity set to the one that Spacy supports then we are slity faster.

#### Accuracy


#### Features

| Feature          | Wowool  |  SpaCy   | Notes                                                                                                               |
|:-----------------|:-------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora         | Yes     | No       | SpaCy does not resolve pronouns like he, she, the city, the company, etc.                                           |
| Conjecture       | Yes     | No       | When Mentioning a something in context, Wowool will remeber that what it was later on                               |
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


Note: google

### Comparing

Notes: we used the `en_core_web_sm` to compare with Wowool, but we noticed that using other models returns inconsistencies during the tests. As some of their own entities disappear and other appeare in other models, so we decided to stick to this model.


### Setup

    pip install Spacy
    python -m Spacy download en_core_web_sm


Using this command you will see the comparison between Spacy and Wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e Spacy


### Results

#### Anaphora

    python3 -m nlp_compare -e Spacy -l english -p "english,entity" -f tests/data/anaphora.text

As we can see Spacy is missing all the references in the second sentence  **Mary Smith** (*she*), **EyeOnText** ( *the IT company* )  and **John Doe** (*he*)

`John Doe and Mary Smith went to work at EyeOnText.`

| uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-----------|------------|------------------|-------------------|
| PERSON    | John Doe   | PERSON           | John Doe          |
| PERSON    | Mary Smith | PERSON           | Mary Smith        |
| ORG       | EyeOnText  | ORG              | EyeOnText         |


`She works for the IT company but he only cleans there.`

| uri_wow   | text_wow   | uri_spacy        | text_spacy        |
|-----------|------------|------------------|-------------------|
| PERSON    | Mary Smith | **Missing**      |                   |
| ORG       | EyeOnText  | **Missing**      |                   |
| PERSON    | John Doe   | **Missing**      |                   |


#### Wrong tagging

As we can see Spacy is incorrectly tagging **the George Washington** missing **John Smith** and missing the location **Washington** from **longtime Washington lawyer**

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

| uri_wow     | text_wow      | uri_spacy        | text_spacy            |
|-------------|---------------|------------------|-----------------------|
| PERSON      | John Smith    | PERSON           | John Smith            |
| **Missing** |               | PERSON           | the George Washington |
| LOC         | Washington    | **Missing**      |                       |
| PERSON      | Eugene Fidell | PERSON           | Eugene Fidell         |
| LOC         | Washington    | GPE              | Washington            |
| GPE         | Washington    | **Missing**      |                       |

`He worked with the president George Washington.`

| uri_wow   | text_wow          | uri_spacy        | text_spacy        |
|-----------|-------------------|------------------|-------------------|
| PERSON    | John Smith        | **Missing**      |                   |
| PERSON    | George Washington | PERSON           | George Washington |
| LOC       | Washington        | **Missing**      |                   |

The first instance is correct, but in the second sentence **Georgia** is tagged as a location (**GPE**) 

`Georgia Smith work in Antwerp.`

| uri_wow     | text_wow      | uri_spacy   | text_spacy    |
|-------------|---------------|-------------|---------------|
| PERSON      | Georgia Smith | PERSON      | Georgia Smith |
| **Missing** |               | GPE         | Antwerpen     |


`Georgia is nice, she does a lot.`

| uri_wow   | text_wow      | uri_spacy   | text_spacy   |
|-----------|---------------|-------------|--------------|
| PERSON    | Georgia Smith | GPE         | Georgia      |
| LOC       | Georgia       | **Missing** |              |
| PERSON    | Georgia Smith | **Missing** |              |

#### Conjecture

As we can see Spacy is incorrectly tagging **Miyaktama** in the second sentence as an organization, although it is clear from the first sentence that it is a Person.

`Mr. Miyaktama Mitshu is a very successful person.`

| uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-----------|------------------|------------------|-------------------|
| PERSON    | Miyaktama Mitshu | PERSON           | Miyaktama Mitshu  |

`Miyaktama is a very good leader.`

| uri_wow   | text_wow         | uri_spacy        | text_spacy        |
|-----------|------------------|------------------|-------------------|
| PERSON    | Miyaktama Mitshu | ORG              | Miyaktama         |

#### Spacy demo sample data

We are testing the sample sentences in the site of Displacy

In this first sentence, the references to **the company** and **him** are lost in Spacy.

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

| uri_wow   | text_wow        | uri_spacy        | text_spacy        |
|-----------|-----------------|------------------|-------------------|
| PERSON    | Sebastian Thrun | PERSON           | Sebastian Thrun   |
| ORG       | Google          | ORG              | Google            |
| CARDINAL  | 2007            | DATE             | 2007              |
| ORG       | Google          | **Missing**      |                   |
| PERSON    | Sebastian Thrun | **Missing**      |                   |


The reference to **Thrun**, who is mentioned in the previous sentence, is lost and the name is wrongly identified as a location. Spacy is also missing **Udacity** as a company, whereas it is clearly identified as a startup.

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

| uri_wow     | text_wow        | uri_spacy        | text_spacy        |
|-------------|-----------------|------------------|-------------------|
| PERSON      | Sebastian Thrun | GPE              | Thrun             |
| ORG         | Udacity         | **Missing**      |                   |
| ORG         | Recode          | ORG              | Recode            |
| **Missing** |                 | DATE             | earlier this week |

#### Hyphenation

    python3 -m nlp_compare -e Spacy -l english -p "english,entity" -f tests/data/hyphenation.txt

As we see, none of these entities are found. Note that this happens a lot with PDF documents that use colums.

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

| uri_wow   | text_wow         | uri_spacy   | text_spacy   |
|-----------|------------------|-------------|--------------|
| GPE       | Antwerp          | **Missing** |              |
| LOC       | Renecarel street | **Missing** |              |
| LOC       | Rivirenhof Park  | **Missing** |              |

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

    pip install Stanza


### Features

#### Speed

Wowool is 50 to a 100 times faster while only using a single core while Stanza is using all cores.

#### Accuracy

Wowool out performs Stanza by far.

#### Features

| Feature          | Wowool  | Stanza   | Notes                                                                                                               |
|:-----------------|:-------:|:--------:|---------------------------------------------------------------------------------------------------------------------|
| Anaphora         | Yes     | No       | Stanza does not resolve pronouns like he, she, the city, the company, etc.                                          |
| Conjecture       | Yes     | No       | When Mentioning a something in context, Wowool will remeber that what it was later on                               |
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
| False Positive's |         |          |                                                                                                                     |
| False Negative's |         |          |                                                                                                                     |

### Comparing

Using this command you will see the comparison between Stanza and Wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e Stanza --show

#### Anaphora

    python3 -m nlp_compare -e Stanza -l english -p "english,entity" -f tests/data/anaphora.txt

First, some speed results:

* Wowool startup time: 0.247
* Stanza startup time: 8.582
* Processing time of Stanza: 0.701 Counter({'PERSON': 2, 'ORG': 1})
* Processing time of Wowool: 0.010 Counter({'PERSON': 4, 'ORG': 2})
* Wowool is 73.213 times faster than Stanza

As we can see Stanza is missing all the references in the second sentence  **Mary Smith** (*she*), **EyeOnText** ( *the IT company* )  and **John Doe** (*he*)

`John Doe and Mary Smith went to work at EyeOnText.`

| uri_wow   | text_wow   | uri_stanza   | text_stanza   |
|-----------|------------|--------------|---------------|
| PERSON    | John Doe   | PERSON       | John Doe      |
| PERSON    | Mary Smith | PERSON       | Mary Smith    |
| ORG       | EyeOnText  | ORG          | EyeOnText     |

`She works for the IT company but he only cleans there.`

| uri_wow   | text_wow   | uri_stanza   | text_stanza   |
|-----------|------------|--------------|---------------|
| PERSON    | Mary Smith | **Missing**  |               |
| ORG       | EyeOnText  | **Missing**  |               |
| PERSON    | John Doe   | **Missing**  |               |

#### Wrong tagging

As we can see Spacy is incorrectly tagging **George Washington** as a location, missing **John Smith**, and missing the location **Washington** from **longtime Washington lawyer**.

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

| uri_wow     | text_wow      | uri_stanza   | text_stanza           |
|-------------|---------------|--------------|-----------------------|
| PERSON      | John Smith    | PERSON       | John Smith            |
| **Missing** |               | GPE          | ~~George Washington~~ |
| LOC         | Washington    | **Missing**  |                       |
| PERSON      | Eugene Fidell | PERSON       | Eugene Fidell         |
| LOC         | Washington    | GPE          | Washington            |
| GPE         | Washington    | **Missing**  |                       |

`He worked with the president George Washington.`

| uri_wow   | text_wow          | uri_stanza   | text_stanza       |
|-----------|-------------------|--------------|-------------------|
| PERSON    | John Smith        | **Missing**  |                   |
| PERSON    | George Washington | PERSON       | George Washington |
| LOC       | Washington        | **Missing**  |                   |

The first instance is correct, but in the second sentence **Georgia** is tagged as a location (**GPE**).


`Georgia is nice, she does a lot.`

| uri_wow   | text_wow      | uri_stanza   | text_stanza   |
|-----------|---------------|--------------|---------------|
| PERSON    | Georgia Smith | ~~GPE~~      | Georgia       |
| *LOC*     | Georgia       | **Missing**  |               |
| PERSON    | Georgia Smith | **Missing**  |               |

**Test:** python3 -m nlp_compare -e Stanza -l english -p "english,entity" -f tests/data/person_wrong_names.txt

#### Conjecture

Stanza is doing better than Spacy in this case, but still loses the reference to **Miyaktama Mitshu**.


`Mr. Miyaktama Mitshu is a very successful person.`

|   beg |   end | uri_wow   | text_wow         | uri_stanza   | text_stanza      |
|-------|-------|-----------|------------------|--------------|------------------|
|     4 |    20 | PERSON    | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu |



`Miyaktama is a very good leader.`

| uri_wow   | text_wow         | uri_stanza   | text_stanza     |
|-----------|------------------|--------------|-----------------|
| PERSON    | Miyaktama Mitshu | PERSON       | *Miyaktama*     |

**Test:** python3 -m nlp_compare -e Stanza -l english -p "english,entity" -f tests/data/person_conjecture.txt

#### Spacy demo sample data.

    python3 -m nlp_compare -e Stanza -l english -p "english,entity" -f tests/data/companies.txt

In this case Stanza split the name **Sebastian Thrun** in two Persons, where it is just one. They are missing **Google** as *the company* and **Sebastian Thrun** as *him* 

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

| uri_wow     | text_wow        | uri_stanza   | text_stanza   |
|-------------|-----------------|--------------|---------------|
| PERSON      | Sebastian Thrun |              |               |
|             |                 | PERSON       | Sebastian     |
|             |                 | PERSON       | Thrun         |
| ORG         | Google          | ORG          | Google        |
| CARDINAL    | 2007            | DATE         | 2007          |
| ORG         | Google          | **Missing**  |               |
| PERSON      | Sebastian Thrun | **Missing**  |               |

* Here they do capture **Udacity** but are wrongly assinging **Recode** as a **WORK_OF_ART**

`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

| uri_wow     | text_wow        | uri_stanza   | text_stanza       |
|-------------|-----------------|--------------|-------------------|
| PERSON      | Sebastian Thrun | PERSON       | Thrun             |
| ORG         | Udacity         | ORG          | Udacity           |
| ORG         | Recode          | WORK_OF_ART  | Recode            |

#### Hyphenation

Stanza does find these entities which have been split with new lines, but the literal has not been resoved or cleandup.

* python3 -m nlp_compare -e Stanza -l english -p "english,entity" -f tests/data/hyphenation.txt


```
I've worked in Ant-
werp in the Rene-
carel street which is close to Riviren-
hof Park.
```

| uri_wow   | text_wow         | uri_stanza   | text_stanza        |
|-----------|------------------|--------------|--------------------|
| GPE       | Antwerp          | **Missing**  |                    |
| LOC       | Renecarel street | FAC          | Rene-\ncarel street |
| LOC       | Rivirenhof Park  | FAC          | Riviren-\nhof Park  |
## Google vs Wowool

First of, there seems to be a bug in GoogleAPI. If an entity is on offset 0 then the REST API does not return an offset in the mentioned object. You can add a space in front of your text, but then all your offsets are off, or you need to add a hack into your code.

#### Anaphora

    python3 -m nlp_compare -e Google -l english -p "english,entity" -f tests/data/anaphora.txt

`John Doe and Mary Smith went to work at EyeOnText.`

| uri_wow      | text_wow   | uri_google   | text_google   |
|--------------|------------|--------------|---------------|
| PERSON       | John Doe   | PERSON       | John Doe      |
| PERSON       | Mary Smith | PERSON       | Mary Smith    |
| ORGANIZATION | EyeOnText  | OTHER        | EyeOnText     |


`She works for the IT company but he only cleans there.`

| uri_wow      | text_wow   | uri_google   | text_google   |
|--------------|------------|--------------|---------------|
| PERSON       | Mary Smith | **Missing**  |               |
| ORGANIZATION | EyeOnText  | **Missing**  |               |
| **Missing**  |            | ORGANIZATION | IT company    |
| PERSON       | John Doe   | **Missing**  |               |

Total:  Time: Google  : 0.303 Counter({'PERSON': 2, 'OTHER': 1, 'ORGANIZATION': 1})
Total:  Time: Wowool  : 0.009 Counter({'PERSON': 4, 'ORGANIZATION': 2})


#### Resolving Entities

As we can see Google is just taking the previous to resolve the CEO and does not look at the context to check the validity.


`Elon Musk is the CEO of SpaceX.`


| uri_wowool   | text_wowool         | uri_google   | text_google     |
|--------------|---------------------|--------------|-----------------|
| PERSON       | Elon Musk           | PERSON       | Elon Musk       |
| PERSON       | the CEO (Elon Musk) | **Missing**  | *the CEO*       |
| POSITION     | CEO                 | PERSON       | CEO (Elon Musk) |
| ORG          | SpaceX              | ORG          | SpaceX          |


`CEO Mark Smith of the company he is responsible for the overall success of the company.`

Elon Musk is NOT the CEO it's Mark Smith, Wowool has the position on the entity *Mark Smith* as a position.

| uri_wowool   | text_wowool          | uri_google   | text_google     |
|--------------|----------------------|--------------|-----------------|
| POSITION     | CEO                  | PERSON       | CEO (Elon Musk) |
| PERSON       | Mark Smith           | PERSON       | Mark Smith      |
| ORG          | the company (SpaceX) | **Missing**  | *the company*   |
|              | *company*            | ORG          | company         |
| PERSON       | he (Mark Smith)      | **Missing**  | *he*            |
| ORG          | the company (SpaceX) | ORG          | *the company*   |


#### Wrong tagging

    python3 -m nlp_compare -e Google -l english -p "english,entity" -f tests/data/person_wrong_names.txt

`John Smith, the George Washington law professor and Eugene Fidell, a longtime Washington lawyer.`

| uri_wow     | text_wow      | uri_google   | text_google       |
|-------------|---------------|--------------|-------------------|
| PERSON      | John Smith    | PERSON       | John Smith        |
| **Missing** |               | PERSON       | George Washington |
| LOCATION    | Washington    | **Missing**  |                   |
| **Missing** |               | ~~PERSON~~   | law professor     |
| Position    | professor     | **Missing**  |                   |
| PERSON      | Eugene Fidell | PERSON       | Eugene Fidell     |
| LOCATION    | Washington    | LOCATION     | Washington        |
| GPE         | Washington    | **Missing**  |                   |
| Position    | lawyer        | ~~PERSON~~   | lawyer            |


`He worked with the president George Washington.`

| uri_wow   | text_wow          | uri_google   | text_google       |
|-----------|-------------------|--------------|-------------------|
| PERSON    | John Smith        | **Missing**  |                   |
| Position  | president         | ~~PERSON~~   | president         |
| PERSON    | George Washington | PERSON       | George Washington |
| LOCATION  | Washington        | **Missing**  |                   |

Total:  Time: Google  : 0.306 Counter({'PERSON': 7, 'LOCATION': 1})
Total:  Time: Wowool  : 0.017 Counter({'PERSON': 4, 'LOCATION': 3, 'Position': 3, 'GPE': 1})

#### Conjecture


    python3 -m nlp_compare -e Google -l english -p "english,entity" -f tests/data/person_conjecture.txt

`Mr. Miyaktama Mitshu is a very successful person.`

| uri_wow     | text_wow         | uri_google   | text_google      |
|-------------|------------------|--------------|------------------|
| **Missing** |                  | ~~PERSON~~   | Mr.              |
| PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama Mitshu |
| **Missing** |                  | PERSON       | person           |


`Miyaktama is a very good leader.`

| uri_wow     | text_wow         | uri_google   | text_google   |
|-------------|------------------|--------------|---------------|
| PERSON      | Miyaktama Mitshu | PERSON       | Miyaktama     |
| **Missing** |                  | ~~PERSON~~       | leader        |

Total:  Time: Google  : 0.815 Counter({'PERSON': 5})
Total:  Time: Wowool  : 0.007 Counter({'PERSON': 2})

#### Spacy demo sample data.

    python3 -m nlp_compare -e Google -l english -p "english,entity" -f tests/data/companies.txt

`When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously.`

| uri_wow      | text_wow        | uri_google   | text_google       |
|--------------|-----------------|--------------|-------------------|
| PERSON       | Sebastian Thrun | PERSON       | Sebastian Thrun   |
| **Missing**  |                 | OTHER        | self-driving cars |
| ORGANIZATION | Google          | ORGANIZATION | Google            |
| **Missing**  |                 | DATE         | 2007              |
| CARDINAL     | 2007            | NUMBER       | 2007              |
| **Missing**  |                 | ~~PERSON~~   | people            |
| ORGANIZATION | Google          | **Missing**  |                   |
| **Missing**  |                 | ORGANIZATION | company           |
| PERSON       | Sebastian Thrun | **Missing**  |                   |


`“I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn't worth talking to.`

| uri_wow     | text_wow   | uri_google   | text_google   |
|-------------|------------|--------------|---------------|
| Position    | CEO        | **Missing**  |               |
| **Missing** |            | PERSON       | CEOs          |
| NORP        | American   | **Missing**  |               |
| **Missing** |            | ~~LOCATION~~     | American      |
| **Missing** |            | ~~ORGANIZATION~~ | car companies |
| **Missing** |            | OTHER        | hand          |


`" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week.`

| uri_wow      | text_wow        | uri_google   | text_google              |
|--------------|-----------------|--------------|--------------------------|
| PERSON       | Sebastian Thrun | **Missing**  |                          |
| **Missing**  |                 | ~~PERSON~~     | Thrun                    |
| Position     | co - founder    | **Missing**  |                          |
| **Missing**  |                 | ~~PERSON~~     | co-founder               |
| Position     | CEO             | **Missing**  |                          |
| **Missing**  |                 | ~~PERSON~~     | CEO                      |
| **Missing**  |                 | ORGANIZATION | higher education startup |
| ORGANIZATION | Udacity         | ORGANIZATION | Udacity                  |
| ORGANIZATION | Recode          | **Missing**  |                          |
| **Missing**  |                 | OTHER        | Recode                   |

Total:  Time: Google  : 0.759 Counter({'PERSON': 6, 'ORGANIZATION': 5, 'OTHER': 3, 'LOCATION': 1, 'EVENT': 1, 'DATE': 1, 'NUMBER': 1})
Total:  Time: Wowool  : 0.025 Counter({'ORGANIZATION': 4, 'PERSON': 3, 'Position': 3, 'NORP': 1})

#### Hyphenation

    python3 -m nlp_compare -e Google -l english -p "english,entity" -f tests/data/hyphenation.txt

Google does find these entities, but the literal has not been resolved and they are confused with the street. **Renecarel street** as they find **Rene** and **street**

    I've worked in Ant-
    werp in the Rene-
    carel street which is close to Riviren-
    hof Park.

| uri_wow     | text_wow         | uri_google   | text_google       |
|-------------|------------------|--------------|-------------------|
| GPE         | Antwerp                 | LOCATION     | Ant-\nwerp |
| LOCATION    | Renecarel street | **Missing**  |                   |
| **Missing** |                  | ~~PERSON~~   | Rene              |
| **Missing** |                  | LOCATION     | street            |
| LOCATION    | Rivirenhof Park  | LOCATION     | Riviren-\nhof Park|


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
| Wowool | english-entity | 14         |               |
| Spacy  | n_core_web_sm  | 15         | <1Mb          |
| Stanza | en             | 1100       |               |

Second, consumed memory:

* Wowool uses 600M to process 1M
* Spacy scales very poorly, giving us the following message `Text of length 1132067 exceeds maximum of 1000000. The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input.`
* Stanza uses a max of 2G

In short, Spacy does not handle big data, and Stanza looks like it does handle bigger data sets but it takes an incredibly long time (718 sec) to process a 1 Mb file, and it uses 11 threads during the process. In contrast, Wowool processed the same input using a single thread in 24 seconds.

### Things that go wrong in unexplainable ways

`Most nonprofits, experts say, don't or can't provide third-party data about the costs and benefits of their interventions.`


| uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|--------------|---------------|-------------|--------------|--------------|---------------|
|              |               | GPE         | n’t          | **Missing**  | *n’t*         |


`The final chapter is, perhaps inevitably, called What to Whole-Arse.`


| uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|--------------|---------------|-------------|--------------|--------------|---------------|
|              |               | PERSON      | Whole-Arse   | **Missing**  | *Whole-Arse*  |


* Date's are random in Spacy and Stanza

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
