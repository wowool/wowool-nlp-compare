### Memory profiling:

For memory and speed profiling I've used scalene. you can just install it using:
There is a small script to run each engine separatly.

    pip install scalene

Note: Could not run on 100k , Stanza was taking to long and finally crashed the profiler at the end, So we used a 10k english file.

#### Wowool

command:

    scalene run_wowool.py -p english,entity  --no-show -f tests/data/sizes/en-10k.txt

![Profile of Wowool](../img/profile_en_10k_wowool.png)

#### Spacy

command:

    scalene run_spacy.py -m en_core_web_sm  --no-show -f tests/data/sizes/en-10k.txt

![Profile of SpaCy](../img/profile_en_10k_spacy.png)

#### Stanza

command:

    scalene run_stanza.py -l en --no-show -f tests/data/sizes/en-10k.txt

![Profile of Stanza](../img/profile_en_10k_stanza.png)
