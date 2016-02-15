# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-10 20:38
# modified : 2014-09-28 12:57
"""
Tokenize Burmish data into phonemes and morphemes.
"""

__author__="Johann-Mattis List"
__date__="2014-09-28"

from lingpyd.plugins.burmish import *
import unicodedata as ucd

def preprocessing(x):
    """
    We define a simple preprocessing of the data here, based on adding split
    symbols to those cases in tokenization where it should be prohibited.
    """
    y = ucd.normalize("NFD",x)

    st = [
            ["ṅḥ","ṅ.ḥ"],
            ["kʐ","k.ʐ"],
            ["m̥ʐ","m̥.ʐ"],
            ["pʐ","p.ʐ"],
            ["phʐ","ph.ʐ"],
            ["xʐ", "x.ʐ"],
            ["hʐ","h.ʐ"],
            ["ky⁵","kÿ⁵"],
            ["mʐ","m.ʐ"],
            ["ñḥ","ñ.ḥ"],
            ["nḥ","n.ḥ"],
            ]
    for i in range(len(st)):
        st[i][0] = ucd.normalize('NFD',st[i][0])
        st[i][1] = ucd.normalize('NFD',st[i][1])

    for s,t in st:
        y = y.replace(s,t)

    return y

wl = Wordlist('burmish.triples')
wl.tokenize(preprocessing=preprocessing)

if 'check_segments' not in wl.header:
    wl.add_entries('check_segments', 'ipa', lambda x: '')
    wl[1][-1] = '!'

test_list = []
too_much = []
missing = []
nasals = []

for k in wl:

    tk = wl[k,'tokens']
    ps = wl[k,'prostring']
    ip = wl[k,'ipa']
    tx = wl[k,'taxon']
    
    if ip not in test_list:
        test_list += [ip]
        if len(tk) < 5 and rc('morpheme_separator') in tk and ps.count('V') == 1:
            if rc('nasal_placeholder') not in tk:
                too_much += [(tx,ip,' '.join(tk),ps)]
        elif ps.count('V') != tk.count(rc('morpheme_separator')) + 1 and \
                rc('nasal_placeholder') not in tk:
            missing += [(tx,ip,' '.join(tk),ps)]

        if '\u0303' in ''.join(tk): # and '\u0303' in ip:
            nasals += [(tx,ip,' '.join(tk),ps)]

too_much = sorted(too_much, key=lambda x: x[0])
missing = sorted(missing, key=lambda x: x[0])
nasals = sorted(nasals, key=lambda x: x[0])
with open('errors_tm.txt', 'w') as f:
    for line in too_much:
        f.write('\t'.join(line)+'\n')
with open('errors_ms.txt', 'w') as f:
    for line in missing:
        f.write('\t'.join(line)+'\n')

with open('nasals_output.txt', 'w') as f:
    for line in nasals:
        f.write('\t'.join(line)+'\n')

ignore = [
        'alignment',
        'scaid',
        'cleaned_entry_a',
        'cluster2id',
        'automatic_tokens'
        ]

wl.update('triples.sqlite3', 'burmish', ignore=ignore)
