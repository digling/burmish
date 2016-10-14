from pyburmish import *
from pyburmish.patterns import get_alignments
from lingpy import *
from lingpy.compare.partial import Partial, _get_slices
from lingpy.settings import rcParams
from pyburmish.phonology import split_tokens
from collections import defaultdict
import networkx as nx
from pyclics.utils import save_network
rcParams['morpheme_separator'] = '+'

def compare_partial_colexifications():
    alms = get_alignments()
    G = nx.Graph()
    for k in alms:
        concept = alms[k, 'concept']
        morphemes = split_tokens(alms[k, 'tokens'])
        doculect = alms[k, 'doculect']
        if concept not in G.node:
            G.add_node(concept, bipartite=0)
        
        for m in morphemes:
            idf = ''.join(m)+'/'+doculect
            if idf not in G.node:
                G.add_node(idf, bipartite=1)
            G.add_edge(concept, idf)
    print('printing now')
    save_network('bipartite.gml', G)
    nodes = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
    G2 = nx.bipartite.collaboration_weighted_projected_graph(G, nodes)
    save_network('projected.gml', G2)
    return G

def search_twins(graph):
    pass

#wl = load_burmish(remote=False, sqlite=False)
#
##part = Partial(wl, check=True)
##part.partial_cluster(method='sca', threshold=0.45)
##part.output('tsv', filename='tmp')
#part = Partial('tmp.tsv')
#blacklist = []
#for k in part:
#    if part[k, 'cogids'].strip() and part[k, 'cogids'] != '0':
#        try:
#            cogs = [int(x) for x in part[k, 'cogids'].split(' ')]
#            part[k][part.header['pcogsets']] = cogs
#        except: 
#            blacklist += [k]
#etd = part.get_etymdict(ref='partial_cognate_sets')
#
#tables = {}
#concepts = {}
#for k, vals in etd.items():
#    filler = []
#    data = False
#    for cogs, taxon in zip(vals, wl.taxa):
#        if cogs and cogs[0] not in blacklist:
#            data = True
#            concepts[k] = part[cogs[0], 'concept']
#            word = part[cogs[0], 'ipa']
#            cogids = part[cogs[0], 'partial_cognate_sets']
#            morpheme = part[cogs[0], 'morphemes']
#            syllables = part[cogs[0], 'tokens']
#            myslice = _get_slices(syllables)[cogids.index(k)]
#            ipa = ''.join(syllables[myslice[0]:myslice[1]])
#            
#            if morpheme and len(morpheme) == len(cogids):
#                morpheme = morpheme[cogids.index(k)]
#            else:
#                morpheme = '???'
#            if not morpheme.strip(): morpheme='???'
#            filler += [(word, ipa+'/'+morpheme)]
#        else:
#            filler += [('Ø', 'Ø')]
#    if data:
#        tables[k] = filler
#text = "cogid | concept | " + ' | '.join(
#        ['{0} | {1} '.format(taxon, 'M') for taxon in wl.taxa])+'\n'
#text += ' --- | --- | '+ ' --- | --- ' * wl.width + '\n'
#for k, val in sorted(tables.items(), key=lambda x: ','.join([y[1] for y in
#    x[1]])):
#    text += '{0} | {1} | '.format(k, concepts[k])
#    text += ' | '.join(['{0} | {1}'.format(a, b) for a, b in val])
#    text += '\n'
#with open(burmish_path('tests', 'colexes.md'), 'w') as f:
#    f.write(text)
#
#
##alm = Alignments(wl, ref='cogids')
##
##idx = 1
##D = {}
##for 
##
##etd = alm.get_etymdict(ref='cogids')
