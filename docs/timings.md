# Timings


## Timeings


CNR = 'could not run'

| Kb    | Wowool | Spacy  | Stanza  | Wowool Kb/sec    | Spacy Kb/sec    | Stanza Kb/sec   |
|-------|--------|--------|---------|------------------|------------------|------------------|
| 1     | 0,031  | 0,047  | 0,835   | 32,258064516129  | 21,2765957446809 | 1,19760479041916 |
| 5     | 0,091  | 0,186  | 2,518   | 54,9450549450549 | 26,8817204301075 | 1,98570293884035 |
| 10    | 0,157  | 0,35   | 5,031   | 63,6942675159236 | 28,5714285714286 | 1,98767640628106 |
| 50    | 0,671  | 1,651  | 23,947  | 74,5156482861401 | 30,2846759539673 | 2,08794421013071 |
| 100   | 1,317  | 3,344  | 47,332  | 75,9301442672741 | 29,9043062200957 | 2,11273557001606 |
| 500   | 6,74   | 16,555 | 244,154 | 74,1839762611276 | 30,2023557837511 | 2,0478878085143  |
| 1000  | 13,97  | 34,946 | 479,118 | 71,5819613457409 | 28,6155783208379 | 2,08716850546212 |
| 2000  | 27,652 | CNR    | 973,859 | 72,3274989150875  | CNR             | 2,05368538977408 |


![Timeings Kb/sec](../img/speed-graph.png)


## Results by size:

### 1k

    Total Time: wowool  : 0.031 Counter({'ORG': 7, 'EVENT': 5, 'GPE': 5, 'PERSON': 4, 'LOC': 2, 'DATE': 1})
    Total Time: spacy   : 0.047 Counter({'ORG': 7, 'GPE': 5, 'DATE': 2, 'PERSON': 2, 'TIME': 1})
    Total Time: stanza  : 0.835 Counter({'GPE': 6, 'ORG': 5, 'PERSON': 4, 'DATE': 3, 'TIME': 1})

* Wowool is 1.5267391893461344 times faster than spacy
* Wowool is 27.120428941968953 times faster than stanza

### 5k

    Total Time: wowool  : 0.091 Counter({'PERSON': 39, 'EVENT': 27, 'GPE': 22, 'ORG': 12, 'LOC': 8, 'DATE': 1})
    Total Time: spacy   : 0.186 Counter({'GPE': 25, 'PERSON': 19, 'ORG': 17, 'DATE': 14, 'TIME': 4})
    Total Time: stanza  : 2.518 Counter({'PERSON': 26, 'GPE': 25, 'DATE': 15, 'ORG': 10, 'TIME': 4})

* Wowool is 2.0421383763305165 times faster than spacy
* Wowool is 27.71395438529289 times faster than stanza

### 10k

    Total Time: wowool  : 0.157 Counter({'PERSON': 52, 'EVENT': 40, 'GPE': 36, 'ORG': 30, 'LOC': 13, 'DATE': 3})
    Total Time: spacy   : 0.350 Counter({'ORG': 41, 'GPE': 33, 'DATE': 28, 'PERSON': 26, 'TIME': 8, 'LOC': 4, 'MONEY': 1})
    Total Time: stanza  : 5.031 Counter({'PERSON': 36, 'GPE': 34, 'ORG': 30, 'DATE': 24, 'TIME': 9, 'LOC': 2, 'MONEY': 1})

* Wowool is 2.2352034942520347 times faster than spacy
* Wowool is 32.09450114594312 times faster than stanza

### 50k

    Total Time: wowool  : 0.671 Counter({'PERSON': 226, 'ORG': 210, 'EVENT': 181, 'GPE': 81, 'LOC': 33, 'DATE': 17})
    Total Time: spacy   : 1.651 Counter({'ORG': 215, 'PERSON': 167, 'DATE': 96, 'GPE': 87, 'TIME': 18, 'LOC': 16, 'MONEY': 4, 'EVENT': 3})
    Total Time: stanza  : 23.947 Counter({'ORG': 211, 'PERSON': 190, 'DATE': 83, 'GPE': 61, 'TIME': 17, 'LOC': 12, 'EVENT': 6, 'MONEY': 2})

* Wowool is 2.461012296343368 times faster than spacy
* Wowool is 35.69693341322864 times faster than stanza

### 100k

    Total Time: wowool  : 1.317 Counter({'PERSON': 566, 'ORG': 449, 'EVENT': 362, 'GPE': 129, 'LOC': 68, 'DATE': 30, 'MONEY': 6})
    Total Time: spacy   : 3.344 Counter({'ORG': 524, 'PERSON': 357, 'DATE': 211, 'GPE': 140, 'LOC': 34, 'TIME': 24, 'MONEY': 13, 'EVENT': 4})
    Total Time: stanza  : 47.332 Counter({'ORG': 472, 'PERSON': 439, 'DATE': 185, 'GPE': 107, 'TIME': 24, 'EVENT': 21, 'LOC': 20, 'MONEY': 9})

* Wowool is 2.5394864425288355 times faster than spacy
* Wowool is 35.939930597797435 times faster than stanza

### 500k

    Total Time: wowool  : 6.740 Counter({'ORG': 2360, 'PERSON': 2188, 'EVENT': 1729, 'GPE': 1002, 'LOC': 336, 'DATE': 136, 'MONEY': 111})
    Total Time: spacy   : 16.555 Counter({'ORG': 2194, 'PERSON': 1460, 'GPE': 1224, 'DATE': 1209, 'LOC': 149, 'MONEY': 131, 'TIME': 108, 'EVENT': 30})
    Total Time: stanza  : 244.154 Counter({'ORG': 1976, 'PERSON': 1761, 'DATE': 1038, 'GPE': 980, 'LOC': 137, 'MONEY': 124, 'TIME': 98, 'EVENT': 65})

* Wowool is 2.4561071262738086 times faster than spacy
* Wowool is 36.223284922798165 times faster than stanza

### 1000k

    Total Time: wowool  : 13.120 Counter({'ORG': 4738, 'PERSON': 4453, 'EVENT': 3417, 'GPE': 2102, 'LOC': 732, 'DATE': 290, 'MONEY': 225})
    Total Time: spacy   : 32.246 Counter({'ORG': 4427, 'PERSON': 2771, 'GPE': 2457, 'DATE': 2454, 'LOC': 283, 'MONEY': 278, 'TIME': 210, 'EVENT': 62})
    Total Time: stanza  : 479.118 Counter({'ORG': 4037, 'PERSON': 3288, 'DATE': 2093, 'GPE': 2084, 'LOC': 269, 'MONEY': 259, 'TIME': 188, 'EVENT': 116})


Results:

* Wowool is 2.4577899632829627 times faster than spacy
* Wowool is 36.51832842531068 times faster than stanza

