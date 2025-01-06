# Google NLP results

As google is a could based service and they do not return -1 for the beginOffset, it was hard to compare with wowool
but here are my findings

## Input Text:

    John Dow and Mary Smith went to work at EyeOnText. She works for the it company but he only cleans there. Mr. Miyaktama Mitshu is a very successful person. Miyaktama is a very good leader. When Sebastian Thrun started working on self-driving cars at Google in 2007 few people outside of the company took him seriously. “I can tell you very senior CEOs of major American car companies would shake my hand and turn away because I wasn't worth talking to.\" said Thrun, now the co-founder and CEO of online higher education startup Udacity, in an interview with Recode earlier this week. EyeOnID has  nice software. The Swedish company is base in Stockholm.

## Findings

* Everything is in desorder.
* Did not get offsets.

### Mistakes

  * Mr. is a **Person**


## Original JSON Results: 

    {
      "entities": [
        {
          "name": "2007",
          "type": "DATE",
          "metadata": {
            "year": "2007"
          },
          "mentions": [
            {
              "text": {
                "content": "2007",
                "beginOffset": -1
              },
              "type": "TYPE_UNKNOWN",
              "probability": 1
            }
          ]
        },
        {
          "name": "2007",
          "type": "NUMBER",
          "metadata": {
            "value": "2007"
          },
          "mentions": [
            {
              "text": {
                "content": "2007",
                "beginOffset": -1
              },
              "type": "TYPE_UNKNOWN",
              "probability": 1
            }
          ]
        },
        {
          "name": "American",
          "type": "LOCATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "American",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.882
            }
          ]
        },
        {
          "name": "CEO",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "CEO",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.878
            }
          ]
        },
        {
          "name": "CEOs",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "CEOs",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.644
            }
          ]
        },
        {
          "name": "EyeOnID",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "EyeOnID",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.429
            }
          ]
        },
        {
          "name": "EyeOnText",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "EyeOnText",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.808
            }
          ]
        },
        {
          "name": "Google",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Google",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.867
            }
          ]
        },
        {
          "name": "John Dow",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "John Dow",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.906
            }
          ]
        },
        {
          "name": "Mary Smith",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Mary Smith",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.894
            }
          ]
        },
        {
          "name": "Miyaktama",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Miyaktama",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.898
            }
          ]
        },
        {
          "name": "Miyaktama Mitshu",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Miyaktama Mitshu",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.906
            }
          ]
        },
        {
          "name": "Mr.",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Mr.",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.882
            }
          ]
        },
        {
          "name": "Recode",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Recode",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.828
            }
          ]
        },
        {
          "name": "Sebastian Thrun",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Sebastian Thrun",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.898
            }
          ]
        },
        {
          "name": "Stockholm",
          "type": "LOCATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Stockholm",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.828
            }
          ]
        },
        {
          "name": "Swedish",
          "type": "LOCATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Swedish",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.859
            }
          ]
        },
        {
          "name": "Thrun",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Thrun",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.859
            }
          ]
        },
        {
          "name": "Udacity",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "Udacity",
                "beginOffset": -1
              },
              "type": "PROPER",
              "probability": 0.878
            }
          ]
        },
        {
          "name": "base",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "base",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.384
            }
          ]
        },
        {
          "name": "car companies",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "car companies",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.894
            }
          ]
        },
        {
          "name": "cars",
          "type": "CONSUMER_GOOD",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "cars",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.289
            }
          ]
        },
        {
          "name": "co-founder",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "co-founder",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.796
            }
          ]
        },
        {
          "name": "company",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "company",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.8
            }
          ]
        },
        {
          "name": "company",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "company",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.886
            }
          ]
        },
        {
          "name": "company",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "company",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.882
            }
          ]
        },
        {
          "name": "hand",
          "type": "OTHER",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "hand",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.82
            }
          ]
        },
        {
          "name": "higher education startup",
          "type": "ORGANIZATION",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "higher education startup",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.41
            }
          ]
        },
        {
          "name": "interview",
          "type": "OTHER",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "interview",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.498
            }
          ]
        },
        {
          "name": "leader",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "leader",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.882
            }
          ]
        },
        {
          "name": "people",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "people",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.914
            }
          ]
        },
        {
          "name": "person",
          "type": "PERSON",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "person",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.886
            }
          ]
        },
        {
          "name": "software",
          "type": "OTHER",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "software",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.439
            }
          ]
        },
        {
          "name": "work",
          "type": "OTHER",
          "metadata": {},
          "mentions": [
            {
              "text": {
                "content": "work",
                "beginOffset": -1
              },
              "type": "COMMON",
              "probability": 0.632
            }
          ]
        }
      ],
      "languageCode": "en",
      "languageSupported": true
    }
