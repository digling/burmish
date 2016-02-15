# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-10 12:44
# modified : 2015-03-10 12:44
"""
Maintenance script for the burmese database.
"""

__author__="Johann-Mattis List"
__date__="2015-03-10"


from lingpyd import *
from lingpyd.plugins.chinese.sinopy import clean_chinese_ipa
from lingpyd.plugins.lpserver.lexibase import LexiBase

# load stb data (today's status)
db = LexiBase('burmish', dbase='burmese.sqlite3',
        #url='http://tsv.lingpy.org/triples/triples.sqlite3'
        )
print(len(db.doculect))
# get all concepts
concepts = []
clist = []
bst = [x[0] for x in csv2list('bst.tsv')]

for i,k in enumerate(sorted(db.concepts)):
    
    # get coverage
    cov = len(set(db.get_list(concept=k, entry='doculect', flat=True)))


    if cov > 9:
        concepts += [(i+1,k,k.replace('the ','').replace('to ',''),cov)]
        clist += [k]

for k in bst:
    if k not in clist:
        clist += [k]

# now that we have the concepts, we can check for coverage on a dialect-basis
taxa = [c for c in db.taxa if c.split('_')[-1] not in 'ABCDE' and 'Proto' not
        in c]

tcov = []
for t in taxa:

    d = db.get_dict(taxa=t)
    l = len([x for x in d if x in clist])
    tcov += [(t,l,l/len(clist))]
ccov = []
for c in clist:

    d = db.get_dict(concept = c)
    l =  len(set([x for x in d if x in taxa]))
    ccov += [(c,l)]

#stbcov = []
#for c in bst:
#
#    d = db.get_dict(concept = c)
#    l =  len([x for x in d if x in taxa])
#    stbcov += [(c,l)]


for c,l in sorted(ccov):
    if l < 5:
        print(c,l)
print('---')


ccovd = dict([(a,b) for a,b in ccov])
for t,l,x in sorted(tcov):

    if x < 0.8:
        print(t,l,x)

print(len(clist))

# make new list
newlist = csv2list('burmish_concepts.tsv')

D = {}
for line in newlist:

    ks = line[2].split(' // ')
    for k in ks:
        D[k] = line[1]

newc = {}
for k in D:
    if k in clist:
        try:
            newc[D[k]] += [k]
        except:
            newc[D[k]] = [k]

idx = 1
with open('burmish_stb_concepts.tsv', 'w') as f:
    f.write('NUMBER\tSTDB\tCONCEPTID\tGLOSS\tCOVERAGE\n')
    for a,b in sorted(newc.items()):
        
        cov = sum([ccovd[x] for x in b])

        if len([x for x in b if x in bst]) > 0:
            f.write(str(idx)+'\t'+'*'+'\t'+a+'\t'+' // '.join(b)+'\t'+str(cov)+'\n')
            idx += 1
        elif sum([ccovd[x] for x in b]) > 6:
            f.write(str(idx)+'\t'+'-'+'\t'+a+'\t'+' // '.join(b)+'\t'+str(cov)+'\n')
            idx += 1









