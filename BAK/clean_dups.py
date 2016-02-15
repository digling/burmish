# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-23 14:27
# modified : 2014-10-23 14:27
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2014-10-23"

from lingpyd.plugins.burmish import *

csv = csv2list('burmish.triples')
for line in csv:
    if len(line) < 3:
        print(line)

wl = Wordlist('burmish.triples')



cn = {}

for concept in wl.concepts:

    orms = wl.get_list(concept=concept, entry='original_concept', flat=True)
    orms = sorted(set(orms))

    cn[concept] = orms


concepts = csv2list('concepts.tsv')
cdic = dict([(a[3],a[2]) for a in concepts[1:]])

wl.add_entries('metagloss','concept', lambda x: x)
for k in wl:
    
    if cdic[wl[k,'original_concept']].startswith('@'):
        nc = wl[k,'original_concept']
    else:
        wl[k][wl.header['concept']] = cdic[wl[k,'original_concept']]

wl.output('tsv', filename='burmish_new_concepts', ignore=['json','taxa'])
wl.output('triples',subset=True, filename='burmish_new_concepts')

wl = Wordlist('burmish_new_concepts.triples')

## get list of original taxa
#ot = {}
#for k in wl:
#    t = wl[k,'taxa']
#    o = wl[k,'original_taxname']
#    try:
#        ot[t][o] += 1
#    except:
#        try:
#            ot[t][o] = 1
#        except:
#            ot[t] = {}
#            ot[t][o] = 1

# reassign taxnames
ot = {'Lashi': {"Lashi (Lachhe') GHL-PPB": 34,
  'Lashi DQ-Lashi': 103,
  'Leqi (Luxi) TBL': 389},
 'Atsi': {'Atsi [Zaiwa] ZMYYC': 168,
  'Atsi [Zaiwa] JZ-Zaiwa': 65,
  'Atsi [Zaiwa] TBL': 398,
  'Atsi [Zaiwa] GHL-PPB': 33},
 'Achang_Longchuan': {'Achang (Longchuan) JZ-Achang': 66,
  'Achang (Longchuan) TBL': 383,
  'Achang (Longchuan) ZMYYC': 161},
 'Maru': {'Langsu (Luxi) TBL': 418,
  'Maru [Langsu] ZMYYC': 181,
  'Maru [Langsu] JO-PB': 23,
  'Maru [Langsu] DQ-Langsu': 87,
  'Maru [Langsu] GHL-PPB': 7},
 'Achang_Lianghe': {'Achang (Lianghe) JZ-Achang': 295},
 'Hpun': {'Hpun (Northern) EJAH-Hpun': 408, 'Hpun (Metjo) GHL-PPB': 40},
 'Xiandao': {'Achang (Xiandao) DQ-Xiandao': 86, 'Achang (Xiandao) TBL': 359},
 'Bola': {'Bola DQ-Bola': 55, 'Bola (Luxi) TBL': 422},
 'Achang_Luxi': {'Achang (Luxi) JZ-Achang': 294},
 'Burmese_ZMYYC': {'Burmese (Written) ZMYYC': 295}}

tnames = {}
for key in ot:

    torder = sorted(ot[key], key = lambda x: ot[key][x],
            reverse=True)
    new_names = []
    for a,t in zip('ABCDEFGHIJKLMN',torder):
        if a != 'A':
            tnames[t] = key+'_'+a
        else:
            tnames[t] = key

wl.add_entries('ndoculect', 'original_taxname', lambda x: tnames[x])
cols = sorted(wl.header, key=lambda x: wl.header[x])
del cols[cols.index('doculect')]

wl.output('tsv', subset=True, cols=cols, filename='burmish_new_taxnames', ignore=['json','taxa'])

wl = Wordlist('burmish_new_taxnames.tsv', col='ndoculect')
cols = sorted(wl.header, key=lambda x: wl.header[x])
del cols[cols.index('ndoculect')]
cols = ['doculect'] + cols
wl.add_entries('doculect', 'ndoculect', lambda x: x)

# get ids marked for deletion
dels = [4096,4097, 2096]
for k in wl:
    checked = wl[k,'check_segments']
    if 'x @lingulist' in checked:
        dels += [k]

wl.output('tsv', subset=True, cols=cols, rows = dict(ID = 'not in '+str(dels)), filename='burmish_new_taxnames',
        ignore=['json', 'taxa'], formatter='concept,doculect')

# third run, now search for possibly identical concepts spread over different
# ids

wl = Wordlist('burmish_new_taxnames.tsv')

# renumber the gloss
wl.renumber('concept')

# search for obvious duplicates, like in HPUN, for example
etd = wl.get_etymdict('original_entry')
dups = []
cvariants = {}
wvariants = {}
for k in etd:

    for entry in etd[k]:
        if entry != 0:
            if len(entry) > 1:
                
                ctmp,wtmp = {},{}
                for idx in entry:
                    
                    # get original concept and the like
                    ocon = wl[idx,'original_concept']
                    ipa = wl[idx,'ipa']

                    try:
                        ctmp[ocon] += [idx]
                    except:
                        ctmp[ocon] = [idx]

                    try:
                        wtmp[ipa] += [idx]
                    except:
                        wtmp[ipa] = [idx]
                
                if len(ctmp) > 1:
                    for idx in entry:
                        cvariants[idx] = sorted(ctmp, key=lambda x:ctmp[x])
                if len(wtmp) > 1:
                    wvariants[entry[0]] = sorted(wtmp, key=lambda x:wtmp[x])
                
                if len(ctmp) == 1:
                    for idx in entry[1:]:
                        dups += [idx]

for k in wl:
    
    if k not in wvariants:
        oen = wl[k,'original_entry'].split('|')
        if len(oen) > 1:
            noen = oen[0]
            varns = False
            if ';' in noen:
                varns = noen.split(';')
            elif ',' in noen:
                varns = noen.split(',')
            elif '~' in noen:
                varns = noen.split('~')
            
            if varns:
                print(varns, [k.strip() for k in varns])
                wvariants[k] = [k.strip() for k in varns]
    
for k in wl:
    if k not in cvariants:
        cvariants[k] = ''
    if k not in wvariants:
        wvariants[k] = ''

wl.add_entries('concept_variants', cvariants, lambda x: ' // '.join(x))
wl.add_entries('form_variants', wvariants, lambda x: ' // '.join(x))


# make homophone index
# search for obvious duplicates, like in HPUN, for example
etd = wl.get_etymdict('ipa')
hvariants = {}
for k in etd:

    for entry in etd[k]:
        if entry != 0:
            if len(entry) > 1:
                
                ctmp = {}
                for idx in entry:
                    
                    # get original concept and the like
                    ocon = wl[idx,'concept']

                    try:
                        ctmp[ocon] += [idx]
                    except:
                        ctmp[ocon] = [idx]
                
                if len(ctmp) > 1:
                    for idx in entry:
                        hvariants[idx] = sorted(ctmp, key=lambda x:ctmp[x])
for k in wl:
    if k not in hvariants:
        hvariants[k] = ''

wl.add_entries('homophones', hvariants, lambda x: ' // '.join(x))
idb = {}
for k in wl:
    idb[k] = str(k)
wl.add_entries('id_back',idb, lambda x: x)
wl.add_entries('check','ipa', lambda x: '-')

clrid = {}
for k in wl:
    clrid[k] = str(wl[k,'clusterid']) + wl[k,'concept']

wl.add_entries('_clusterid',clrid, lambda x: x)

wl.renumber('_clusterid', 'cogid')

cols = [k for k in sorted(wl.header, key=lambda x: wl.header[x]) if not
        k.startswith('_')]
del cols[cols.index('check_segments')]
del cols[cols.index('concept_key')]




wl.output('tsv', filename='burmish_new', subset=True, cols=cols,rows=dict(ID = 'not in '+str(dups)), ignore=['json', 'taxa'], formatter='concept,doculect')

csv = csv2list('burmish_new.tsv')

with open('burmish.tsv', 'w') as f:
    
    f.write('\t'.join(csv[0])+'\n')
    count = 1
    for line in csv[1:]:
        f.write(str(count)+'\t'+'\t'.join(line[1:])+'\n')
        count += 1

