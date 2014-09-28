# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-10 19:49
# modified : 2014-09-10 21:17
"""
Wordlist plugin for burmish data.
"""

__author__="Johann-Mattis List"
__date__="2014-09-10"

import unicodedata as ucd
import re
import sqlite3
import lingpyd

from .unicode import *


def clean_entry(entry, **keywords):
    """
    Normalize (NFC) entry and remove bad chars.
    """

    kw = dict(
            brackets = rcParams['brackets'],
            exact_bracket_matching = True,
            )
    kw.update(keywords)

    # normalize first
    new_entry = ucd.normalize("NFD", entry)

    # normalize linguistically
    entries = list(new_entry)
    for i,char in enumerate(entries):
        try:
            entries[i] = rcParams['normalizations'][char]
        except KeyError:
            pass
    new_entry = ''.join(entries)
    
    if kw['exact_bracket_matching']:
        # delete stuff in brackets
        for b1 in kw['brackets']:
            b2 = get_pendant(b1)
            
            # get possible index
            idxA = new_entry.find(b1)
            idxB = new_entry.find(b2)

            # check for existing indices
            if idxA != -1 and idxA < idxB:
                new_entry = new_entry[:idxA]+new_entry[idxB+1:]
    else:
        b1s = []
        b2s = []
        for b1 in kw['brackets']:
            idxA = new_entry.find(b1)
            if idxA != -1:
                b1s.append(idxA)
            idxB = new_entry.find(get_pendant(b1))
            if idxB != -1:
                b2s.append(idxB)

        new_entry = new_entry[:min(b1s)]+new_entry[max(b2s)+1:]

    # go for spaces and replace by '_'
    new_entry = new_entry.replace(' ','_')
    
    return new_entry

def ipa2tokens(
        istring,
        **keywords
        ):
    """
    Tokenize IPA-encoded strings. 
    
    Parameters
    ----------

    seq : str
        The input sequence that shall be tokenized.
    
    diacritics : {str, None} (default=None)
        A string containing all diacritics which shall be considered in the
        respective analysis. When set to *None*, the default diacritic string
        will be used.
    
    vowels : {str, None} (default=None)
        A string containing all vowel symbols which shall be considered in the
        respective analysis. When set to *None*, the default vowel string will
        be used.

    tones : {str, None} (default=None)
        A string indicating all tone letter symbals which shall be considered
        in the respective analysis. When set to *None*, the default tone string
        will be used.

    combiners : str (default="\u0361\u035c")
        A string with characters that are used to combine two separate
        characters (compare affricates such as t͡s).

    breaks : str (default="-.")
        A string containing the characters that indicate that a new token
        starts right after them. These can be used to indicate that two
        consecutive vowels should not be treated as diphtongs or for diacritics
        that are put before the following letter.
    
    merge_vowels : bool
        Indicate, whether vowels should be merged into diphtongs
        (default=True), or whether each vowel symbol should be considered
        separately.

    merge_identical_symbols : bool
        Indicate, whether identical symbols should be merged into one token, or
        rather be kept separate.

    Returns
    -------
    tokens : list
        A list of IPA tokens.


    Examples
    --------
    >>> from lingpyd import *
    >>> myseq = 't͡sɔyɡə'
    >>> ipa2tokens(myseq)
    ['t͡s', 'ɔy', 'ɡ', 'ə']
    
    See also
    --------
    tokens2class
    class2tokens
    """
    # go for defaults
    kw = dict(
            vowels = lingpyd.settings.rcParams['vowels'],
            diacritics = lingpyd.settings.rcParams['diacritics'],
            expand_nasals = True, # addon
            tones = lingpyd.settings.rcParams['tones'],
            combiners = lingpyd.settings.rcParams['combiners'],
            breaks = lingpyd.settings.rcParams['breaks'],
            stress = lingpyd.settings.rcParams['stress'],
            merge_vowels = lingpyd.settings.rcParams['merge_vowels'],
            merge_identical_symbols = True,
            )
    kw.update(keywords)

    # clean the entry first
    istring = clean_entry(istring)

    # check for pre-tokenized strings
    if ' ' in istring:
        out = istring.split(' ')
        if istring.startswith('#'):
            return out[1:-1]
        else:
            return out
    
    # create the list for the output
    out = []

    nasals = "ãũẽĩõ"
    nasal_char = "\u0303"
    semi_diacritics = "ʃhsʑɕʂʐñ"
    nogos = '_'
    
    # set basic characteristics
    vowel = False # no vowel
    tone = False # no tone
    merge = False # no merge command
    start = True # start of unit
    nasal = False # start of nasal vowel environment

    for char in istring:

        # check for nasal stack and vowel environment
        if nasal:
            if char not in kw['vowels'] and char not in kw['diacritics'] :
                out += [rcParams['nasal_placeholder']]
                nasal = False
                
        # check for breaks first, since they force us to start anew
        if char in kw['breaks']:
            start = True
            vowel = False
            tone = False
            merge = False
        
        # check for combiners next
        elif char in kw['combiners']:
            out[-1] += char
            merge = True

        # check for stress
        elif char in kw['stress']:
            out += [char]
            # XXX be careful about the removement of the start-flag here, but it
            # XXX seems to make sense so far!
            merge = True
            tone = False
            vowel = False
            start = False
        
        # check for merge command 
        elif merge:
            out[-1] += char
            if char in kw['vowels']:
                vowel = True
            merge = False

        # check for nasals 
        elif kw['expand_nasals'] and char == nasal_char and vowel:
            out[-1] += char
            start = False
            nasal = True

        # check for weak diacritics
        elif char in semi_diacritics and not start and not vowel and not tone and out[-1] not in nogos:
            out[-1] += char
        
        # check for diacritics
        elif char in kw['diacritics']:
            if not start:
                out[-1] += char
            else:
                out += [char]
                start = False
                merge = True
        
        # check for vowels
        elif char in kw['vowels']:
            if vowel and kw['merge_vowels']:
                out[-1] += char
            else:
                out += [char]
                vowel = True
            start = False
            tone = False
        
        # check for tones
        elif char in kw['tones']:
            vowel = False
            if tone:
                out[-1] += char
            else:
                out += [char]
                tone = True
            start = False

        # consonants
        else:
            vowel = False
            tone = False
            out += [char]
            start = False
            tone = False
    
    if nasal:
        out += [rcParams['nasal_placeholder']]

    if kw['merge_identical_symbols']:
        new_out = [out[0]]
        for i in range(len(out) -1):
            outA = out[i]
            outB = out[i+1]
            if outA == outB:
                new_out[-1] += outB
            else:
                new_out += [outB]
        return new_out

        
    return out

def secondary_structures(tokens):
    """
    Function handles the tokenization of strings into secondary structures.
    """
    segment = rcParams['morpheme_separator']

    pstring = lingpyd.prosodic_string(tokens)
    
    # check for more than one vowel in the set
    vlen = pstring.count('X')+pstring.count('Z')+pstring.count('Y')
    if vlen == 1: return tokens
    elif vlen == 2 and rcParams['nasal_placeholder'] in tokens:
        return tokens

    out = []
    tmp_tokens = list(zip(tokens, 
        lingpyd.prosodic_string(tokens)
        ))
    
    new_syllable = True
    while tmp_tokens:

        token,prochar = tmp_tokens.pop(0)
        
        # check for tonal pro-chars
        if prochar == 'T'  and len(tmp_tokens) != 0:
            out += [token, segment]
            new_syllable = True

        elif prochar == '_' and tmp_tokens and not new_syllable:
            out += [segment]
            new_syllable = True

        elif prochar == '_' and len(out) > 1 and out[-1] == segment:
            new_syllable = True

        # check for markers if no tone is given
        elif prochar == 'B' and not new_syllable and tmp_tokens:
            if out[-1] == 'A':
                out += [token]
            else:
                out += [segment,token]

        # if nothing else is given, just append the string
        else:
            out += [token]
            new_syllable = False
    
    return out



class Wordlist(lingpyd.basic.wordlist.Wordlist):

    def __init__(self, infile):
        
        if infile.endswith('.triples'):
            D = lingpyd.basic.ops.triple2tsv(infile, output='dict')

            lingpyd.basic.wordlist.Wordlist.__init__(self, D)
        else:
            lingpyd.basic.wordlist.Wordlist.__init__(self,infile)
    
    def tokenize(self, override=True, preprocessing=False):

        if not preprocessing:
            preprocessing = lambda x: x

        self.add_entries('tokens', 'ipa', lambda x:
                ipa2tokens(preprocessing(x)),override=override)

        self.add_entries('prostring','tokens', lambda x: lingpyd.prosodic_string(x,
            _output='CcV'), override)

        self.add_entries('tokens', 'tokens', lambda x: secondary_structures(x),
                override = override)
    
    def update(self, dbase, table, ignore=False):
        """
        Upload triple-data to sqlite3-db.
        """
        if not ignore: ignore=[]
        # get the triples
        triples = lingpyd.basic.ops.tsv2triple(self,False)
        
        # connect to tatabase
        db = sqlite3.connect(dbase)
        cursor = db.cursor();
        cursor.execute('drop table '+table+';')
        cursor.execute('create table '+table+' (ID int, COL text, VAL text);')
        cursor.execute('vacuum')
        for a,b,c in triples:
            if b.lower() not in ignore:
                if type(c) == list:
                    c = ' '.join([str(x) for x in c])
                else:
                    c = str(c)
                cursor.execute('insert into '+table+' values (?, ?, ?);', (a, b, c))
        db.commit()

