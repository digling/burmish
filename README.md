Burmish
=======

A LingPy plugin for handling concrete datasets.

Weblinks
========

* General URL of Wordlist Editor (EDICTOR): http://tsv.lingpy.org 
* Customized URL for Burmish data (CHECK SEGMENTATION-STAGE): http://tsv.lingpy.org/?css=menu:show,textfields:show,database:show,&formatter=CLUSTERID&preview=10&basics=DOCULECT,CONCEPT,IPA,CHECKSEGMENTS,ORIGINALENTRY,TOKENS,&pinyin=CHINESE&highlight=TOKENS&file=burmish
* Link to our issue tracker: https://github.com/LinguList/burmish/issues

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
