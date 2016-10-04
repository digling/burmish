from clldutils.dsv import UnicodeReader
import os
from pyconcepticon.api import Concepticon
from functools import partial
from lingpy._plugins.lpserver.lexibase import LexiBase
from collections import OrderedDict

def load_concepticon():

    concepticon = dict([
        (line['ID'], line) for line in Concepticon().conceptsets()
        ])

    return concepticon

def burmish_path(*comps):
    """
    Our data-path in CLICS.
    """
    return os.path.join(os.path.dirname(__file__), os.pardir, *comps)

def load_burmish(remote=False):
    
    if not remote:
        db = LexiBase('burmish', dbase=burmish_path('sqlite', 'burmish.sqlite3'))
    else:
        db = LexiBase('burmish', dbase=burmish_path('sqlite',
            'burmish.sqlite3'), 
            url='burmish.sqlite3')
    return db

def load_concepts(idf):
    with UnicodeReader(burmish_path('concepts', idf+'-concepts.tsv'), delimiter='\t') as reader:
        data = list(reader)
    concepts = {}
    for line in data[1:]:
        if line[1] in concepts:
            print(line[1])
        concepts[line[1]] = OrderedDict(zip(data[0], line))
    return concepts

def load_csv(*paths, delimiter='\t'):
    with UnicodeReader(burmish_path(*paths), delimiter=delimiter) as reader:
        return list(reader)
