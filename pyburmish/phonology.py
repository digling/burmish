from pyburmish import *
from lingpy._plugins.chinese import sinopy as sp
from collections import defaultdict
import networkx as nx

def split_tokens(tokens, separator='+'):
    out = [[]]
    for k in tokens:
        if k == separator:
            out += [[]]
        else:
            out[-1] += [k]
    return out

def phonostats():
    wl = load_burmish(sqlite=False, remote=False)
    stats = {}
    for k in wl.taxa:
        stats[k] = defaultdict(dict)
        
    for t in wl.taxa:
        table, initials, medials, nuclei, finals, tones = initials_and_rhymes(t)
        stats[t]['initials'] = initials
        stats[t]['medials'] = medials
        stats[t]['nuclei'] = nuclei
        stats[t]['codas'] = finals
        stats[t]['tones'] = tones
        stats[t]['finals'] = sorted(table)

        uniques = set()
        for tokens in wl.get_list(taxon=t, entry='tokens', flat=True):
            uniques.add(' '.join(tokens))
        stats[t]['uniques'] = uniques
    return stats

def format_phonostats(phonostats):
    text = 'Variety\tInitials\tMedials\tNuclei\tCodas\tTones\n'
    for variety in sorted(phonostats):
        text += '\t'.join(['{0}'.format(x) for x in [
            variety,
                    len(phonostats[variety]['initials']),
                    len(phonostats[variety]['medials']),
                    len(phonostats[variety]['nuclei']),
                    len(phonostats[variety]['codas']),
                    len(phonostats[variety]['tones'])]])+'\n'
    return text
    

def initials_and_rhymes(variety):
    wl = load_burmish(sqlite=False, remote=False)
    if variety is None:
        variety = wl.taxa[0]
    table = defaultdict(dict)
    initials = set()
    medials = set()
    nuclei = set()
    finals = set()
    tones = set()

    for idx in wl.get_list(col=variety, flat=True):
        tokens = wl[idx, 'tokens']
        for syllable in split_tokens(tokens):
            try:
                splits = sp.parse_chinese_morphemes(syllable)
                i, m, n, f, t = splits
                initials.add(i)
                medials.add(m)
                nuclei.add(n)
                finals.add(f)
                tones.add(t)
                try:
                    table[tuple(splits[1:-1])][i] += [idx]
                except KeyError:
                    table[tuple(splits[1:-1])][i] = [idx]
            except:
                print('Error in {0}, {1}'.format(' '.join(syllable), idx))
    return (table, sorted(initials), sorted(medials), sorted(nuclei), sorted(finals), 
            tones)

def format_the_table(table, initials, medials, nuclei, finals, tones):
    text = 'M\tN\tF\t'+'\t'.join(initials)+'\n'
    for ((m, n, f),vals) in table.items():
        text += '{0}\t{1}\t{2}\t'.format(m, n, f)
        _tmp = []
        for _i in initials:
            if _i in vals:
                _tmp += [str(len(vals[_i]))]
            else:
                _tmp += ['']
        text += '\t'.join(_tmp)+'\n'
    return text

def make_bipartite(table):
    G = nx.Graph()
    for k, v in table.items():
        G.add_node(' '.join(k), bipartite=0, occ=sum([len(table[k][vv]) for vv in
            table[k]]))
        for val, occ in v.items():
            if not val in G.node:
                G.add_node(val, bipartite=1, occ=len(occ))
            else:
                G.node[val]['occ'] += len(occ)

            G.add_edge(' '.join(k), val, weight=len(occ))
    return G

def articulation_points(graph):
    return graph, nx.articulation_points(graph)

