# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-23 14:27
# modified : 2014-11-06 17:06
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2014-11-06"

from lingpyd.plugins.burmish import *

csv = csv2list('burmish.triples')
for line in csv:
    if len(line) < 3:
        print(line)

wl = Wordlist('burmish.triples')


wl.output('tsv',filename='burmish')

wl = Wordlist('burmish.tsv')

# assemble cognate sets
etd = wl.get_etymdict(ref="cogid")

# setup dictionary for alignments
alms = {}

# start the loop and fill in dictionary
for k in etd:
    
    print('aligning cogset number {0}'.format(k))
    if k != 0:
        tokens = []
        idxs = []
        for idx in etd[k]:
            if idx != 0:
                idx = idx[0]

                if wl[idx,'taxa'] not in ['Old_Burmese']:
                    tokens += [wl[idx,'tokens']]
                    idxs += [idx]
                elif wl[idx,'taxa'] in ['Old_Burmese']:
                    print(wl[idx,'tokens'])
                    if wl[idx,'tokens'][0] not in ['0','?']:
                        ttokens = wl[idx,'tokens']
                        ntok = []
                        for t in ttokens:
                            if t in '₁₂':
                                ntok[-1] += t
                            elif t == '_':
                                ntok += ['◦']
                            else:
                                ntok += [t]
                        tokens += [ntok]
                        wl[idx][wl.header['tokens']] = ntok
           
                        idxs += [idx]
                    else: print(wl[idx,'tokens'])
        
        if len(tokens) > 1:
            m = Multiple(tokens)
            m.lib_align(restricted_chars='_')
            
            for idx,alm in zip(idxs,m.alm_matrix):

                alms[idx] = ' '.join(alm)

for k in wl:
    if k not in alms:
        alms[k] = ''

    if wl[k,'tokens'][0] == '0':
        wl[k][wl.header['tokens']] = '?'
    if wl[k,'ipa'] == '0':
        wl[k][wl.header['ipa']] = '?'

wl.add_entries('alignment',alms, lambda x: x)
wl.output('tsv', filename='burm_aligned')

wl.update('../dbase/triples.sqlite3', 'burmish')
print("Updating successful")
