# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-05-13 10:41
# modified : 2015-05-13 10:41
"""
Re-organize all concepts, but first get a list of the stedt-concepts
"""

__author__="Johann-Mattis List"
__date__="2015-05-13"


from lingpyd import *
from lingpyd.sequence.sound_classes import syllabify
from lingpyd.plugins.lpserver import lexibase as lb

# load the lexibase
db = lb.LexiBase(
            'burmish',
            dbase='burmish.sqlite3',
            url='http://tsv.lingpy.org/triples/burmish.sqlite3'
        )

# now get the taxa for TBL
tbl_taxa = []
tbl_concepts = []
other_concepts = []
for k in db:
    taxon = db[k,'taxon']
    source = db[k,'source']
    concept = db[k,'stedt_concept']
    srcid = db[k,'stedt_srcid'].split('.')[0]
    if source == 'TBL':
        if taxon not in tbl_taxa:
            tbl_taxa += [taxon]
        if (concept,srcid) not in tbl_concepts:
            tbl_concepts += [(concept,srcid)]
    else:
        if concept not in other_concepts:
            other_concepts += [concept]

with open('other_concepts.tsv', 'w') as f:
    f.write('NUMBER\tGLOSS\n')
    for i,c in enumerate(other_concepts):
        f.write('{0}\t{1}\n'.format(i+1,c))

stdb_concepts = csv2list('stdb-concepts.tsv')
stdb_cdict = dict([(x[-1],x[1]) for x in stdb_concepts[1:]])

# now check for current coverage
idx = 1
tbl_cdict = dict([(x[1],x[0]) for x in tbl_concepts])
concept_labels = {}
for c,s in tbl_concepts:
    if s in stdb_cdict:
        print(idx,c,s,stdb_cdict[s])
        idx += 1
        concept_labels[s] = stdb_cdict[s]
    else:
        concept_labels[s] = c

idx = 1
missing_concepts = {}
for s,c in stdb_cdict.items():
    if s not in tbl_cdict:
        print(idx,c,s)
        idx += 1
        missing_concepts[s] = c
    concept_labels[s] = c

# now we need to add the missing data from the tbl
tbl = Wordlist('tbl_ipa.tsv')
tbl.add_entries('tokens', 'ipa', lambda x: syllabify(
    ipa2tokens(x, expand_nasals=True)))
print("Loaded TBL data")
# get mapping between the taxa
burm2tbl = {
        'Achang_Longchuan' : 'Achang (Longchuan)',
        'Atsi' : 'Atsi [Zaiwa]',
        'Lashi' : 'Leqi (Luxi)',
        'Maru': 'Langsu (Luxi)',
        'Xiandao': 'Achang (Xiandao)',
        'Rangoon' : 'Burmese (Rangoon)',
        'Written_Burmese' : 'Burmese (Written)',
        'Bola' : 'Bola (Luxi)',
        }
tbl2burm = dict([(x[1],x[0]) for x in burm2tbl.items()])

# identify missing source id concepts 
concepts2add = []
for k in tbl:
    srcid = tbl[k,'srcid'].split('.')[0]
    concept = tbl[k,'concept']
    taxon = tbl[k,'doculect']
    if srcid in missing_concepts and taxon in tbl2burm:
        if concept not in concepts2add:
            concepts2add += [concept]

# now we have them and can start browsing the data accordingly
D = {}
for concept in concepts2add:
    
    # get the data
    data = tbl.get_dict(concept=concept)
    for stedt_taxon,burmish_taxon in tbl2burm.items():
        try:
            idxs = data[stedt_taxon]
            for idx in idxs:
                reflex = tbl[idx,'reflex']
                ipa = tbl[idx,'ipa']
                tokens = tbl[idx,'tokens']
                srcid = tbl[idx,'srcid'].split('.')[0]
                stedt_id = idx
                source = 'TBL'
                try:
                    stdb_concept = concept_labels[srcid]
                    
                    D[idx] = [
                            burmish_taxon,
                            stedt_taxon,
                            stdb_concept,
                            concept,
                            reflex,
                            ipa,
                            tokens,
                            source,
                            stedt_id,
                            tbl[idx,'srcid'],
                            srcid
                            ]
                except KeyError:
                    pass
        except:
            print(concept,stedt_taxon)
D[0] = [
        'doculect',
        'original_taxname',
        'concept',
        'original_concept',
        'original_entry',
        'ipa',
        'tokens',
        'source',
        'stedt_rn',
        'stedt_srcid',
        'concept_id',
        ]

wl = Wordlist(D)
wl.output('tsv', filename='data2add-2015-05-13')

db.add_data(wl)


for k in db:

    source = db[k,'source']
    if source == 'TBL':
        try:
            db[k][db.header['concept']] = concept_labels[db[k,'concept_id']]
            print('success',db[k,'concept'])
        except:
            db[k][db.header['concept']] = db[k,'original_concept']
            print('failure', db[k,'concept'])

db.create('burmish')

import os
os.system('mv burmish.sqlite3 ~/projects/websites/dighl/triples/')

# make the website
# in later steps:
# re-link the data
txt1 = ''
concepts = sorted(set([db[k,'concept'] for k in db]))
# get stdb-concepts
stdb249 = [x[1] for x in stdb_concepts[1:]]

for c in concepts:
    
    # determine coverage
    cov = len([db[k,'concept'] for k in db if db[k,'concept'] == c])
    if c in stdb249:
        txt1 += '<option value="'+c+'" selected>'+c+' ('+str(cov)+')</option>'
    else:
        txt1 += '<option value="'+c+'">'+c+'('+str(cov)+')</option>'

txt2 = ''
langs = [db[k,'taxon'] for k in db]
langs = sorted(set(langs))

for k in langs:
    if k in tbl_taxa:
        txt2 += '<option value="'+k+'" selected>'+k+'</option>'
    else:
        txt2 += '<option value="'+k+'">'+k+'</option>'

txt3 = ''
for col in sorted(db.header, key=lambda x: db.header[x]):
    txt3 += '<option value="'+col.upper()+'" selected>'+col.upper()+'</option>'

with open('website/index.template.html') as f:
    d = f.read()
    d = d.format(JS=open('website/stb.js').read(), 
            DOCULECTS = txt2,
            CONCEPTS  = txt1,
            CONTENT = txt3
            )
with open('website/index.html', 'w') as f:
    f.write(d)        
