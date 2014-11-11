Burmish
=======

A LingPy plugin for handling concrete datasets.

Weblinks
========

* General URL of Wordlist Editor (EDICTOR): http://tsv.lingpy.org 
* Customized URL for Burmish data (CHECK SEGMENTATION-STAGE): http://tsv.lingpy.org/?css=menu:show,textfields:show,database:show,&formatter=COGID&preview=10&basics=DOCULECT,CONCEPT,IPA,ORIGINALENTRY,TOKENS,ALIGNMENT,COGID&pinyin=CHINESE&highlight=TOKENS,ALIGNMENT&file=burmish
* 
* Link to our issue tracker: https://github.com/LinguList/burmish/issues

Things to be kept in mind (based on closed issues)
==================================================

We have 

* problems handling brackets or "variants" in the data, where people use the form "a(x)" to denote that both the form "a" and the form "ax" may be attested (or what was their original intention?)
* the initial automatic procedure of extracting words by similar meaning and cleanign entries for segmentation ignore that the semi-colon is also used as a separator between dictionary entries. These cases have now been cleaned manually, but this means that some intereseting word forms (there are after all 39 cases in which a semi-colon was used), may not be in the data right now. However, all data can be retrieved by checking the "original entry" column of the data, which is what should anyway be done when dealing with doubtful cases.

Workflow
========

The workflow is not fixed at the moment and will change, depending on problems we face during the reconstruction procedure. 
At the moment, are in the stage of 

* SEGMENTATION (phonological and morphological)

Before that, some initial steps were conducted, including:

* SEMANTIC TAGGING
* AUTOMATIC COGNATE ASSIGNMENT
* INITIAL (MANUAL) COGNATE ASSIGNMENT
* AUTOMATIC ALIGNMENT OF PARTIAL COGNATES

The next step after SEGMENTATION will be to remove DUPLICATES (due to the fact that data came from multiple sources for particular "doculects") and refine SEMANTIC TAGGING (there are some errors in the current version).

Generally, we try to more or less take the following workflow as orientation:

![Workflow](https://raw.githubusercontent.com/LinguList/burmish/master/workflow.jpg)

This workflow is basically iterative, so we will jump back and forth whenever needed. In all steps, we will first try to find automatic solutions and then apply manual corrections afterwards. So this workflow is computer-guided, not automatic!
