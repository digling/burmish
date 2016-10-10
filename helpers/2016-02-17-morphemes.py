from lingpy import *
from lingpy.sequence.sound_classes import tokens2morphemes
import networkx as nx

wl = Wordlist('../tsv/burmish.tsv')

G = nx.Graph()
txt = ''
for taxon in wl.taxa:

    M = {}
    data = wl.get_dict(taxon=taxon, flat=True)
    words = []
    syllables = []
    for c,idxs in data.items():
    
        for idx in idxs:
            tokens = wl[idx, 'tokens']
            words += [' '.join(tokens)]
            morphemes = tokens2morphemes(tokens, output='nested')
            for i,morpheme in enumerate(morphemes):
                syllables += [' '.join(morpheme)]
                try:
                    M[' '.join(morpheme)] += [(c, idx, i)]
                except KeyError:
                    M[' '.join(morpheme)] = [(c, idx, i)]
    
    # add morpheme information
    for m,v in M.items():
        for i, (c1, idx1, pos1) in enumerate(v):
            for j, (c2, idx2, pos2) in enumerate(v):
                if i < j:
                    try:
                        G.edge[c1][c2]['weight'] += 1
                        G.edge[c1][c2]['words'] += [(idx1,pos1, idx2, pos2)]
                    except KeyError:
                        G.add_edge(c1, c2, weight=1, words=[(idx1,pos1, idx2,
                            pos2)])
    
    txt += '\n# Morpheme Information for {0}\n'.format(taxon)
    txt += '## Statistics\n'
    txt += '* {0} unique syllables\n* {1} syllables\n* {2} unique words\n* {3} words \n\n'.format(
            len(set(syllables)), len(syllables), len(set(words)), len(words))
    txt += '## Recurring Morphemes (n > 2)\n'
    txt += '| morpheme | idf | concept | word |\n'
    txt += '| -------- | --- | ------- | ---- |\n'
    singletons = []
    for k,v in sorted(M.items(), key=lambda x: len(x[1])):
        if len(v) > 1:
            for c, idx, pos in v:
                print(k,'\t',idx,'\t',c)
                txt += '| {0} | {1} | {2} | {3} |\n'.format(
                        k,
                        idx,
                        c,
                        ' '.join(wl[idx,'tokens']).replace(
                            k,
                            '**'+k+'**'
                            ))
            txt += '| -------- | --- | ------- | ---- |\n'
        else:
            singletons += [(k,)+v[0]]
    
        print('')
    txt += '## Singleton Morphemes\n'
    txt += '| morpheme | idf | concept | word |\n'
    txt += '| -------- | --- | ------- | ---- |\n'
    for k, c, idx, pos in sorted(singletons, key=lambda x: x[1]):
        txt += '| {0} | {1} | {2} | {3} |\n'.format(
                        k,
                        idx,
                        c,
                        ' '.join(wl[idx,'tokens']).replace(
                            k,
                            '**'+k+'**'
                            ))

with open('../morphemes/morphemes.md', 'w') as f:
    f.write(txt)

txt = '# Partial Colexifications in the Burmese Data\n'
txt += '| concept 1 | concept 2 | language | word 1 | word 2 |\n'
txt += '| --------- | --------- | -------- | ------ | ------ |\n'
for c1, c2, data in sorted(G.edges(data=True), key=lambda x: (x[0], x[1],
    x[2]['weight'])):
    if data['weight'] < 3:
        pass
    else:
        for idx1, pos1, idx2, pos2 in data['words']:
            morpheme = tokens2morphemes(wl[idx1,'tokens'])[pos1]
            if 'a' in morpheme[0] or 'ɑ' in morpheme[0] and len(morpheme) < 3:
                pass
            else:
                tmp = '{0}\t{1}\t{2}\t{3}\t{4}'.format(
                        c1, c2, wl[idx1, 'language'], 
                        ' '.join(wl[idx1,'tokens']).replace(
                            ' '.join(tokens2morphemes(wl[idx1,'tokens'])[pos1]),
                            '**'+' '.join(tokens2morphemes(wl[idx1,'tokens'])[pos1])+'**'
                            ),
                        ' '.join(wl[idx2,'tokens']).replace(
                            ' '.join(tokens2morphemes(wl[idx2,'tokens'])[pos2]),
                            '**'+' '.join(tokens2morphemes(wl[idx2,'tokens'])[pos2])+'**'
                            )
                        )
                print(tmp)
                txt += '| '+tmp.replace('\t',' | ')
                txt += ' |\n'

with open('../morphemes/colexifications.md', 'w') as f:
    f.write(txt)
