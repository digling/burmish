from clldutils.dsv import UnicodeReader
import os
from pyconcepticon.api import Concepticon
from functools import partial
from lingpy._plugins.lpserver.lexibase import LexiBase
from lingpy import *
from collections import OrderedDict
from urllib import request
import zlib

from pyburmish.data import url

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

def load_burmish(remote=False, sqlite=True):
    
    if sqlite:
        if not remote:
            db = LexiBase('burmish', dbase=burmish_path('sqlite', 'burmish.sqlite3'))
        else:
            db = LexiBase('burmish', dbase=burmish_path('sqlite',
                'burmish.sqlite3'), 
                url='burmish.sqlite3')
        return db
    else:
        if not remote:
            wl = Wordlist(burmish_path('dumps', 'burmish.tsv'),
                    conf=burmish_path('conf', 'wordlist.rc'))
            return wl
        else:
            download()
            return load_burmish(remote=False, sqlite=False)

def download(target='url'):
    if target == 'url':
        with request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open(burmish_path('dumps', 'burmish.tsv'), 'w') as f:
            f.write(data)
            
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

def check_burmish():
    wl = load_burmish(sqlite=False, remote=False)
    print('Database has {0} words for {1} languages and {2} concepts.'.format(
        len(wl), wl.width, wl.height))

def language_coverage():
    wl = load_burmish(sqlite=False, remote=False)
    for key, value in sorted(wl.coverage().items()):
        print('{0:20}: {1}'.format(key, value))


