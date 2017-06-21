from lingpy import *
from pyburmish import *
from collections import defaultdict
from lingpy.sequence.sound_classes import tokens2morphemes

wl = Wordlist(burmish_path('dumps', 'burmish.tsv'))
etd = wl.get_etymdict(ref='cogids')
proto_concepts = defaultdict(set)
cogids = {}
cidx = 1
for k, vals in etd.items():
    idxs = []
    for v in vals:
        if v:
            idxs += v
    concepts = sorted(set([wl[idx, 'concept'] for idx in idxs]))
    for idx, concept in enumerate(concepts):
        tmp = concept+'-'+str(k)
        if tmp in cogids:
            pass
        else:
            cogids[tmp] = cidx
            cidx += 1
for idx in wl:
    cogids_ = wl[idx, 'cogids']
    print(wl[idx, 'concept'], cogids_)
    wl[idx, 'cogids'] = [cogids[wl[idx, 'concept']+'-'+str(x)] for x in cogids_]
    print(cogids_, wl[idx, 'cogids'])

for idx, cogids, tokens, doculect, concept in iter_rows(wl, 'cogids', 'tokens',
        'doculect', 'concept'):
    print(idx, doculect, concept, tokens)
    cls = tokens2class(tokens, 'cv')
    morphemes = tokens2morphemes(tokens, sep="+")
wl.output('tsv', filename=burmish_path('burmish-proto'))
alm = Alignments(burmish_path('burmish-proto.tsv'), ref='cogids',
        alignment='alignments')
etd = alm.get_etymdict(ref='cogids')
for k, vals in etd.items():
    idxs = [v[0] for v in vals if v]
    concept = alm[idxs[0], 'concept']
    proto_concepts[concept].add(k)
    
alm.align()
cons = alm.get_consensus(ref='cogids', counterpart='tokens', return_data=True,
        gaps=True)
proto = {}
idx = max(wl)+1
for concept, vals in proto_concepts.items():
    vals = sorted(vals)
    print(vals)
    vorder = [len([x[0] for x in etd[v] if x]) for v in vals]
    dsorted = sorted(
            zip(
                vals,
                vorder,
                [cons[x] for x in vals]), 
            key=lambda x: x[1], reverse=True)
    pids = [v[0] for v in dsorted]
    tks = [v[2] for v in dsorted]
    vorder = [v[1] for v in dsorted if v[1] > 2]
    
    tokens = ' + '.join([' '.join(t) for t in tks[:len(vorder)]])
    pids = pids[:len(vorder)]
    print(tokens, pids)
    if vorder:
        proto[idx] = [concept, [t for t in tokens.split(' ') if t != '-'], tokens, pids]
        idx += 1
D = {
        0: ['doculect', 'concept', 'ipa', 'tokens', 'cogids', 'alignment']
        }
for idx, d, c, i, t, cogs, a in iter_rows(alm, 'doculect', 'concept', 'ipa',
        'tokens', 'cogids', 'alignments'):
    D[idx] = [d, c, i, t, cogs, a]
for idx, (a, b, c, d) in proto.items():
    D[idx] = ['Proto-Burmish', a, ''.join(b), ' '.join(b), d, c]
wl = Wordlist(D)
wl.output('tsv', filename=burmish_path('dumps', 'burmish-proto'))
