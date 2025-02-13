# NLP compare

##  Usage

To run the tool simply call:

    python3 -m nlp_compare -e spacy,stanza,googel -l english -p "english,entity" -f tests/data/hyphenation.txt

* -e, --engines  : The engine you want to compare , currently support for spacy,stanza,google
* -l, --language : The language to run
* -p, --pipeline : This is the wowool pipeline.
* -f, --file : The file you want to run.
* -a : the list of annotation we want to compare.

All the sample files are located in test/data/

**Note** that all the test have been done with google nlp, so if you do not have access just remove it from the *-e* option

## Features 

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


***Test:***  python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/anaphora.txt -a "Sentence,PERSON,ORG,POS,GPE,LOC"


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

***Test:***  python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/person_conjecture.txt -a "Sentence,PERSON,ORG,POS,GPE,LOC"


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

***Test:***  python3 -m nlp_compare -e spacy,stanza,google -l english -p "english,entity" -f tests/data/normalization.txt -a "Sentence,PERSON,ORG,POS,GPE,LOC"

### Spacy.io Demo text

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

### Sample Sentence

`Frank McCourt told CNN on Thursday that while ByteDance's bankers have confirmed receipt of his group's offer, he expected the company was waiting to hear what the Supreme Court does.`


### Spacy

| ?   |   beg |   end | uri_wowool   | URI_wowool   | text_wowool   | uri_spacy   | URI_spacy   | text_spacy        |
|-----|-------|-------|--------------|--------------|---------------|-------------|-------------|-------------------|
| ~   |     0 |    13 | PERSON       | Person       | Frank Mccourt | PERSON      | PERSON      | Frank McCourt     |
|     |    19 |    22 | ORG          | Publisher    | CNN           | ORG         | ORG         | CNN               |
|     |    46 |    55 | ORG          | Company      | ByteDance     | ORG         | ORG         | ByteDance         |
| -   |   111 |   113 | PERSON       | Person       | Frank Mccourt | **Missing** |             | *he*              |
| -   |   123 |   134 | ORG          | Company      | ByteDance     | **Missing** |             | *the company*     |
| ~   |   164 |   177 | ORG          | Organization | Supreme Court | ORG         | ORG         | the Supreme Court |

### Stanza

`Frank McCourt told CNN on Thursday that while ByteDance's bankers have confirmed receipt of his group's offer, he expected the company was waiting to hear what the Supreme Court does.`


| ?   |   beg |   end | uri_wowool   | URI_wowool   | text_wowool         | uri_stanza   | URI_stanza   | text_stanza       |
|-----|-------|-------|--------------|--------------|---------------------|--------------|--------------|-------------------|
| ~   |     0 |    13 | PERSON       | Person       | Frank Mccourt       | PERSON       | PERSON       | Frank McCourt     |
|     |    19 |    22 | ORG          | Publisher    | CNN                 | ORG          | ORG          | CNN               |
|     |    46 |    55 | ORG          | Company      | ByteDance           | ORG          | ORG          | ByteDance's       |
| -   |   111 |   113 | PERSON       | Person       | Frank Mccourt       | **Missing**  |              | *he*              |
| -   |   123 |   134 | ORG          | Company      | ByteDance           | **Missing**  |              | *the company*     |
| ~   |   158 |   171 | ORG          | Organization | Supreme Court       | ORG          | ORG         | the Supreme Court |


### Google

`Frank McCourt told CNN on Thursday that while ByteDance's bankers have confirmed receipt of his group's offer, he expected the company was waiting to hear what the Supreme Court does.`

| uri_wowool   | URI_wowool   | text_wowool         | uri_google   | URI_google   | text_google       |
|--------------|--------------|---------------------|--------------|--------------|-------------------|
| PERSON       | Person       | Frank Mccourt       | PERSON       | PERSON       | Frank McCourt     |
| ORG          | Publisher    | CNN                 | ORG          | ORG          | CNN               |
| ORG          | Company      | ByteDance           | ORG          | ORG          | ByteDance         |
| POSITION     | Position     | banker              | PERSON       | PERSON       | Frank McCourt     |
| PERSON       | Person       | Frank Mccourt       | **Missing**  |              | *he*              |
| ORG          | Company      | ByteDance           | ORG          | ORG          | company           |
| ORG          | Organization | Supreme Court       | ORG          | ORG         | the Supreme Court  |


## Things that go wrong in unexplainable ways

### Names (snippets from news)

`Most nonprofits, experts say, don't or can't provide third-party data about the costs and benefits of their interventions.`

| uri_wowool   | text_wowool   | uri_spacy   | text_spacy   | uri_stanza   | text_stanza   |
|--------------|---------------|-------------|--------------|--------------|---------------|
|              |               | **GPE**         | **n’t**          |              |               |


`The final chapter is, perhaps inevitably, called What to Whole-Arse.`

| uri_wowool   | text_wowool   | uri_spacy   | text_spacy     | uri_stanza   | text_stanza   |
|--------------|---------------|-------------|----------------|--------------|---------------|
|              |               | **PERSON**  | **Whole-Arse** |              |               |

There are many more !

### Date's are random in Spacy and Stanza

Depending on the date it's a cardinal or a date ! not very usefull if you have to figure it yourself.

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

### Companies

`His physical makeover for Maga reasons, performing music because no one will stop him, trying to look cool on a surfboard - all these are extremely difficult to watch.`


| ?   |   beg |   end | uri_wowool   | text_wowool     | uri_stanza   | text_stanza   |
|-----|-------|-------|--------------|-----------------|--------------|---------------|
| x   |  3404 |  3408 |              | *Maga*          | PERSON       | Maga          |

`This lifted shares of other luxury goods makers such as LVMH and Kering in France, and the UK's Burberry .`


| ?   |   beg |   end | uri_wowool   | text_wowool                 | uri_stanza   | text_stanza         |
|-----|-------|-------|--------------|-----------------------------|--------------|---------------------|
| x   |   710 |   729 |              | *the UK’s   Burberry*       |  **ORG !**   | the UK’s   Burberry |
| -   |   714 |   716 | **GPE**      | UK                          |              | *UK*                |
| -   |   721 |   729 | **ORG**      | Burberry                    |              | *Burberry*          |

`Morgan Stanley made a profit of $3.7bn in the fourth quarter of last year, up from $1.5bn a year earlier.`

Spacy is tagging 'Morgan Stanley' as a Person and *Stanley* as a ORG ! while wowool is tagging *Morgan Stanley* as a company.

| ?   |   beg |   end | uri_wowool   | text_wowool    | uri_stanza   | text_stanza      |
|-----|-------|-------|--------------|----------------|--------------|------------------|
| -   |  7350 |  7364 | **ORG**      | Morgan Stanley |              | *Morgan Stanley* |
| x   |  7350 |  7356 |              | *Morgan*       | **PERSON !** | Morgan           |
| x   |  7357 |  7364 |              | *Stanley*      | **ORG**      | Stanley          |