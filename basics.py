# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-10 19:49
# modified : 2014-09-10 19:49
"""
Wordlist plugin for burmish data.
"""

__author__="Johann-Mattis List"
__date__="2014-09-10"

import lingpyd

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
            merge_vowels = lingpyd.settings.rcParams['merge_vowels']
            )
    kw.update(keywords)

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
    nasal = "\u0303"
    semi_diacritics = "ʃhsʑɕʂʐ"
    
    # set basic characteristics
    vowel = False # no vowel
    tone = False # no tone
    merge = False # no merge command
    start = True # start of unit

    for char in istring:
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
        elif kw['expand_nasals'] and char == nasal:
            out[-1] += char
            out += ["∼"]
            start = False
            merge = False

        # check for nasal vowels
        elif char in nasals:
            out += [char]
            out += ["∼"]
            start = False
            merge = False

        # check for weak diacritics
        elif char in semi_diacritics and not start and not vowel:
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

    return out

class Wordlist(lingpyd.basic.wordlist.Wordlist):

    def __init__(self, infile):
        
        if infile.endswith('.triples'):
            D = lingpyd.basic.ops.triple2tsv(infile, output='dict')

            lingpyd.basic.wordlist.Wordlist.__init__(self, D)
        else:
            lingpyd.basic.wordlist.Wordlist.__init__(self,infile)
    
    def tokenize(self, override=True):

        self.add_entries('tokens', 'ipa', lambda x:
                ipa2tokens(x.replace(' ','_'),override=override))

