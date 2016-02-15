Burmish
=======

A LingPy plugin for handling concrete datasets.

Weblinks
========

* General URL of Wordlist Editor (EDICTOR): http://tsv.lingpy.org 
* Customized URL for Burmish data (CHECK SEGMENTATION-STAGE): http://tsv.lingpy.org/?css=menu:show,textfields:show,database:show,&formatter=COGID&preview=10&basics=DOCULECT,CONCEPT,IPA,ORIGINALENTRY,TOKENS,ALIGNMENT,COGID&pinyin=CHINESE&highlight=TOKENS,ALIGNMENT&file=burmish
* 
* Link to our issue tracker: https://github.com/LinguList/burmish/issues

News
====

Added full support for the languages now, that is, we have all glottocodes, the sources in STEDT, etc. 
I also added an automatically generated [geographic map](https://github.com/LinguList/burmish/blob/master/json/languages.geojson) that shows all languages on github, for which coordinates could be found on Glottolog.

All languages in the sample along with meta-data, and additional information can now be found [under this link](https://github.com/dighl/burmish/blob/master/tsv/doculects.tsv). Note that both Hpun and Marma are not really in the current sample, since we need to map their concepts first to the list of 250 concepts we have selected (and potentially also to the larger list to be selected later).

Workflow
========

We need to re-arrange our workflow as follows:

1. update three missing concepts in the data which were now added to the Sino-Tibetan database (calculation already done, update pending, but not difficult)
2. decide for a larger list of concepts on the basis of TBL data (since this is the largest source)
3. (potentially at the same time with 2) check all phonetic entries in the current data, there by 
4. carry out a full morpheme analysis for each of the languages in the sample. That means: Assign for all morphemes in the word entries which ones are internally cognate.
5. carry out partial cognate assignment, potentially with help of automatic preparsing procedure. This has been partially done in the past, but we need to check to which degree it is consistent, and we need to merge this with the language-internal morphological analysis, which is indispensible for all further tasks.


Further steps we need
