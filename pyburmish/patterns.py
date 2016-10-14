from lingpy import *
from lingpy.align.sca import get_consensus, SCA
from collections import defaultdict
import networkx as nx
from itertools import combinations
from pyclics.utils import save_network
from pyburmish import *
from pyburmish.util import *
from pyburmish.phonology import split_tokens
from lingpy.settings import rcParams

rcParams['morpheme_separator'] = '+'

def clean_tokens(tokens, refine=None):
    out = []
    if not refine:
        refine = {
                'xʐ': ['x', 'ʐ'],
                'mʐ': ['m', 'ʐ'],
                'm̥ʐ': ['m̥', 'ʐ'],
                'kʐʰ': ['kʰ', 'ʐ'],
                'kʐ': ['k', 'ʐ'],
                '†_': [],
                '†au' : ['au'],
                'kh' : ['kʰ'],
                #'†ɲ̇' : [
                }
    
    for t in tokens:
        if not t.strip():
            pass
        else:
            out += refine.get(t, [t])
    return out

def make_alignments(verbose=False):
        
    wl = load_burmish(sqlite=False, remote=False)
    blacklist = []
    renumber = {0: 0}
    for k in wl:
        cogids = wl[k, 'cogids'].strip()
        concept = wl[k, 'concept']
        wl[k][wl.header['tokens']] = clean_tokens(wl[k, 'tokens'])
        if not cogids or cogids == 0:
            blacklist += [(k, '?')]
        else:
            tokens = clean_tokens(wl[k, 'tokens'])
            morphemes = split_tokens(tokens)
            if '0' in tokens2class(tokens, 'sca'):
                blacklist += [(k, '0')]
            elif len(morphemes) != len(cogids.split(' ')):
                blacklist += [(k, 'M')]
            else:
                for c in cogids.split(' '):
                    cogid = c+':'+concept
                    if cogid not in renumber:
                        new_val = max(renumber.values())+1
                        renumber[cogid] = new_val
                    else:
                        pass
    C = {}
    blist = [k[0] for k in blacklist]
    for k in wl:
        if k not in blist:
            C[k] = [renumber[c+':'+wl[k, 'concept']] for c in wl[k,
                'cogids'].split()]
        else:
            C[k] = [0]
    wl.add_entries('pcogids', C, lambda x: x)
    D = {}
    D[0] = [h for h in sorted(wl.header, key=lambda x: wl.header[x]) if h not
            in ['alignment']]
    for k in wl:
        if k not in blacklist:
            D[k] = [wl[k, h] for h in D[0]]
    if verbose: print(D[0])
    alm = Alignments(D, ref='pcogids', conf=burmish_path('conf',
            'wordlist.rc'))
    if verbose: print(alm._mode)
    if verbose:
        for cogid, msa in alm.msa['pcogids'].items():
            sca = SCA(msa)
            sca.prog_align()
    alm.align(method='library', iterate=True)
    alm.output('tsv', filename=burmish_path('dumps', 'alignments'),
        ignore='all', prettify=False)
    for i, (k, r) in enumerate(blacklist):
        if wl[k, 'cogids']:
            print(i+1, r, k, wl[k, 'concept'], wl[k, 'doculect'], wl[k,
                'tokens'], repr(wl[k, 'cogids']))
    
def get_alignments(ref='pcogids'):
    return Alignments(burmish_path('dumps', 'alignments.tsv'), ref=ref,
            conf=burmish_path('conf', 'wordlist.rc'))


def pattern_consensus(patterns):
    out = []
    for i in range(len(patterns[0])):
        col = [line[i] for line in patterns]
        no_gaps = [x for x in col if x != 'Ø']
        if len(set(no_gaps)) > 1:
            #print(no_gaps, patterns)
            raise ValueError
        out += [no_gaps[0] if no_gaps else 'Ø']
    return out

def compatible_columns(colA, colB, gap='-'):
    matches = 0
    for a, b in zip(colA, colB):
        if not gap in [a, b]:
            if a != b:
                return -1
            else:
                matches += 1
    return matches

def strict_compatibility_graph(wordlist, ref='partial_ids', pos='T', mintax=3,
        verbose=False, use_taxa=["Old_Burmese", "Burmese", "Written_Burmese",
        "Rangoon", "Achang_Longchuan", "Xiandao", "Lashi", "Atsi", "Bola", "Maru"]):
    if [x for x in use_taxa if x not in wordlist.taxa]:
        raise ValueError("Your list of taxa contains taxa not in the wordlist.")
    G = nx.Graph()
    stats = [0, 0]
    alignments, cogids, cstrings = [], [], []
    for cogid, msa in wordlist.msa[ref].items():
        taxa = msa['taxa']
        if len(set(taxa)) >= mintax:
            stats[0] += 1
            consensus = get_consensus(msa['alignment'], gaps=True)
            prostring = prosodic_string(consensus)
            pidx = prostring.find(pos)
            if pidx != -1:
                stats[1] += 1
                reflexes = []
                for t in use_taxa:
                    if t not in taxa:
                        reflexes += ['Ø']
                    else:
                        reflexes += [msa['alignment'][taxa.index(t)][pidx]]
                alignments += [reflexes]
                cogids += [cogid]
                cstrings += [consensus[pidx]]
                G.add_node(str(cogid), column = ' '.join(alignments[-1]),
                        consensus=consensus[pidx], clique=0, cliquesize=0,
                        color = tokens2class(consensus, color)[0], 
                        fuzzy=[]
                        )
    if verbose: 
        print('Patterns in total: {0}\nPatterns with condition: {1}'.format(stats[0], 
            stats[1]))
        input('<OK>')

    for (cogA, colA, consA), (cogB, colB, consB) in combinations(
            zip(cogids, alignments, cstrings), r=2):
        cc = compatible_columns(colA, colB, gap="Ø")
        if cc > 0:
            G.add_edge(str(cogA), str(cogB), weight=cc)

    # find cliques
    cliques = [x for x in sorted(nx.find_cliques(G), key=lambda x: len(x),
        reverse=False) if len(x) > 1]

    # assign to clique with highest compatibility
    clique_dict = {}
    for i, clique in enumerate(cliques):
        weight = 0
        for nA, nB in combinations(clique, r=2):
            weight += G.edge[nA][nB]['weight']
        clique_dict[i+1] = weight / len(clique)
    
    # assemble fuzzy nodes
    for i, clique in enumerate(cliques): 
        for node in clique:
            G.node[node]['fuzzy'] += [i+1]
    
    # assign to clique with highest compatibility
    for i,(n, d) in enumerate(sorted(G.nodes(data=True))):
        if d['fuzzy']:
            cliques = sorted(d['fuzzy'],
                    reverse=True,
                    key=lambda x: clique_dict[x])
            G.node[n]['clique'] = cliques[0]
            G.node[n]['cliquesize'] = clique_dict[cliques[0]]
            G.node[n]['fuzzy'] = cliques

    # recount number of cliques
    current_cliques = defaultdict(list)
    for n, d in G.nodes(data=True):
        if d['clique']:
            current_cliques[d['clique']] += [n]

    # recalculate weights
    nclique_dict = {}
    for clique, nodes in current_cliques.items():
        weight = 0
        for nA, nB in combinations(nodes, r=2):
            weight += G.edge[nA][nB]['weight']
        nclique_dict[clique] = weight / len(nodes)
    for n, d in G.nodes(data=True):
        if d['clique']:
            fuzzies = sorted(d['fuzzy'], key=lambda x: nclique_dict.get(x, 0),
                reverse=True)
            d['clique'] = fuzzies[0]
            d['cliquesize'] = nclique_dict[fuzzies[0]]

    # make a compatibility check again for all cliques with each other
    # recount number of cliques
    current_cliques = defaultdict(list)
    for n, d in G.nodes(data=True):
        if d['clique']:
            current_cliques[d['clique']] += [n]
    new_nodes = {}
    visited = []
    for (c1, nodes1), (c2, nodes2) in sorted(
            combinations(current_cliques.items(), r=2), key=lambda x: (
                len(x[0][1]), len(x[1][1]))):
        if c1 not in visited and c2 not in visited:
            nnodes1 = new_nodes.get(c1, nodes1)
            nnodes2 = new_nodes.get(c2, nodes2)
            # consensus 1
            cons1 = pattern_consensus([G.node[n]['column'].split(' ') for n in nnodes1])
            cons2 = pattern_consensus([G.node[n]['column'].split(' ') for n in nnodes2])
            comp = compatible_columns(cons1, cons2, gap='Ø')
            if comp > 0:
                if len(nnodes1) > len(nnodes2) and len(nnodes1) >= 1:
                    for n in nnodes2:
                        G.node[n]['clique'] = c1
                    new_nodes[c1] = nnodes1 + nnodes2
                    new_nodes[c2] = nnodes1 + nnodes2
                    visited += [c1, c2]
                    #print('merged', c1, c2)
                    #for n in new_nodes[c1]:
                    #    print(G.node[n]['column'])
                    #input()
                elif len(nnodes2) > len(nnodes1) and len(nnodes1) >= 1:
                    for n in nodes1:
                        G.node[n]['clique'] = c2
                    new_nodes[c1] = nnodes1 + nnodes2
                    new_nodes[c2] = nnodes1 + nnodes2
                    visited += [c1, c2]
                    #print(':merged', c2, c1)
                    #for n in new_nodes[c1]:
                    #    print(G.node[n]['column'])
                    #input()
    # re-calculate cliques and weights
    current_cliques = defaultdict(list)
    for n, d in G.nodes(data=True):
        if d['clique']:
            current_cliques[d['clique']] += [n]
    # recalculate weights
    nclique_dict = {}
    for clique, nodes in current_cliques.items():
        weight = 0
        for nA, nB in combinations(nodes, r=2):
            weight += G.edge[nA][nB]['weight'] if nB in G.edge[nA] else 0
        nclique_dict[clique] = weight / len(nodes)
    # determine clique sizes
    for node, data in G.nodes(data=True):
        data['fuzzy'] = '/'.join(sorted([str(x) for x in data['fuzzy']]))
        if data['clique']:
            data['cliquesize'] = nclique_dict[data['clique']]
    for node, data in G.nodes(data=True):
        data['commons'] = '{0}-{1}'.format(data['cliquesize'], data['clique'])

    return G, nclique_dict

def extract_patterns(alms, G, context, ref='pcogids', verbose=False):
    patterns = defaultdict(list)
    out = []
    for node, data in G.nodes(data=True):
        concept = alms[alms.msa[ref][int(node)]['ID'][0], 'concept']
        patterns[data['clique']] += [(node, concept, data['column'].split(' '))]
    for i, (p, vals) in enumerate(sorted(patterns.items(), key=lambda x: len(x[1]),
            reverse=True)):
        if len(vals) >= 3:
            cols = [x[2] for x in vals]
            #for c in cols:
            #    print('\t'.join(c))
            #print('')
            concepts = ' / '.join([x[1] for x in vals])
            cogids = ' / '.join([str(x[0]) for x in vals])
            try:
                consensus = pattern_consensus(cols)
                out += [[p, context, len(vals), cogids, concepts]+consensus]
            except ValueError:
                pass
                #print('Error with {0} / {1}'.format(str(cogids),
                #    ','.join(concepts)))
                #input()
    return out

def collapsible_patterns(alms, G, context, ref='pcogids', verbose=False,
        use_taxa=["Old_Burmese", "Burmese", "Written_Burmese",
        "Rangoon", "Achang_Longchuan", "Xiandao", "Lashi", "Atsi", "Bola", "Maru"]):
    if [x for x in use_taxa if x not in alms.taxa]:
        raise ValueError("Your list of taxa contains taxa not in the wordlist.")
    patterns = defaultdict(list)
    for node, data in G.nodes(data=True):
        concept = alms[alms.msa[ref][int(node)]['ID'][0], 'concept']
        words = []
        msa = alms.msa[ref][int(node)]
        for i, t in enumerate(use_taxa):
            if t in msa['taxa']:
                words += [''.join(msa['seqs'][msa['taxa'].index(t)]).replace('-','')]
            else:
                words += ['Ø']
        patterns[data['clique']] += [(node, concept, words)]
    collapsible = defaultdict(list)
    for pattern, vals in patterns.items():
        g = nx.Graph()
        for n, c, words in vals:
            collapsible[pattern, tuple(words)] += [(n, c)]
            g.add_node(n, c=c, w=words)
        for (n1, c1, words1), (n2, c2, words2) in combinations(vals, r=2):
            if compatible_columns(words1, words2, gap='Ø') >= 1:
                g.add_edge(n1, n2)
        for clique in nx.find_cliques(g):
            if len(clique) > 1:
                for n in clique:
                    print(pattern, '{0:4}'.format(n), 
                            '{0:22}'.format(g.node[n]['c'][:21]),
                            '   '.join(['{0:6}'.format(x) for x in
                                g.node[n]['w']]))
                print('--')

def cgraph_to_html(alms, G, context, cdict, verbose=False, ref='pcogids', 
        use_taxa=["Old_Burmese", "Burmese", "Written_Burmese",
        "Rangoon", "Achang_Longchuan", "Xiandao", "Lashi", "Atsi", "Bola", "Maru"]):
    """
    convert graph to html for inspection
    """
    if [x for x in use_taxa if x not in alms.taxa]:
        raise ValueError("Your list of taxa contains taxa not in the wordlist.")
    
    txt = '<html><head><meta charset="utf8"></meta></head><body><table style="border:2px solid black;"'
    previous = 0
    regular = 0
    for node, data in sorted(G.nodes(data=True), 
            key=lambda x: (x[1]['clique'], x[1]['cliquesize'], x[1]['consensus'])):
        current = data['clique']
        if data['cliquesize'] >= 2:
            regular += 1
            if current != previous:
                if verbose: print('---')
                txt += '<tr><th colspan="9"><hr style="border:2px solid gray;align:center;height:2px;color=black" /></th></tr>'
                txt += '<tr><th>PATTERN: {0}</th>'.format(data['clique'])
                txt += ''.join(['<th style="font-family:monospace;">'+t[:4]+'</th>' for t in use_taxa])+'</tr>'
                previous = current
            if verbose: print(node, '\t{0:4}'.format(data['clique']), '\t', ' '.join(
                ['{0:4}'.format(y) for y in data['column'].split(' ')]))
            
            # get the concept
            concept = alms[alms.msa[ref][int(node)]['ID'][0], 'concept']
            txt += '<tr><td style="font-weight:bold">&quot;{1}&quot;, ID: {0} </td>'.format(node,
                    concept)
            for j, cell in enumerate(data['column'].split(' ')):
                taxon = use_taxa[j]
                ncell = cell
                try:
                    alm_idx = alms.msa[ref][int(node)]['taxa'].index(taxon)
                    word = ''.join(alms.msa[ref][int(node)]['seqs'][alm_idx])
                    if is_aspirated_or_unvoiced(word):
                        ncell = ncell+'/H'
                    if is_creaky(word):
                        if not '/' in ncell:
                            ncell = ncell + '/!'
                        else:
                            ncell = ncell +'!'

                except:
                    word = 'Ø'
            
                txt += '<td data-word="{3}" data-letter="{1}" title="{2}" onmouseover="this.innerHTML=this.dataset[\'word\'];" onmouseout="this.innerHTML=this.dataset[\'letter\'];" style="cursor:grab;border:1px solid gray;width:30px;background-color:{0}">{1}</td>'.format(
                    tokens2class([cell], color)[0],
                    ncell,
                    use_taxa[j],
                    word
                    )
            txt += '</tr>'
    txt +='</table></body></html>'
    with open(burmish_path('plots', 'corrs-{0}.html'.format(context)), 'w') as f:
        f.write(txt)
    if verbose: print(regular)
