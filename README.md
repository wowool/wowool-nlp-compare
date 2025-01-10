# NLP compare

This tool allows us to compare different nlp engines with the wowool engine.

## Setup

    pip install -r wowool-requirements.txt

## Spacy vs Wowool

### Setup

    pip install spacy
    python -m spacy download en_core_web_sm
  
### Comparing

Notes: we used the `en_core_web_sm` to compare with wowool, but we noticed that using other models returns inconsistencies during the tests. As some of their own entities disapeared and other appeared in other models, so we decided to stick to the one model.

Using this command you will see the comparison between spacy and wowool in speed and accuracy.

    python3 -m nlp_compare -l english -p "english,entity" -f test.txt -e spacy

This command will generate 2 files:

* `wowool-vs-spacy-tbl.txt`: Table with the entities side by side 
* `wowool-vs-spacy-diff.txt`: Fiff beween the two result files

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

In this project, we compared various Natural Language Processing (NLP) engines to evaluate their performance on different tasks. The key findings are as follows:

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

