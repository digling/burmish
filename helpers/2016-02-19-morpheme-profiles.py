from lingpy import *
from lingpy.sequence.sound_classes import tokens2morphemes
import networkx as nx
import markdown

wl = Wordlist('../tsv/burmish.tsv')

G = nx.Graph()
txt = ''
MO = {}
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
    MO[taxon] = M
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




# now add the profiles
txt = ''
for taxon in wl.taxa:
    txt += '# Morpheme Profiles for Taxon {0}\n'.format(taxon)
    concepts = wl.get_dict(taxon=taxon)
    for c in [x for x in wl.concepts if x in concepts]:
        idxs = concepts[c]
        words = [wl[k,'tokens'] for k in idxs]
        for this_idx, word in zip(idxs, words):
            txt += '**"{0}" [{1}], {2}**\n\n'.format(c, ' '.join(word), this_idx)
            morphemes = tokens2morphemes(word)
            flatlist = [[] for x in morphemes]
            for i, morpheme in enumerate(morphemes):
                for concept, idx, pos in MO[taxon][' '.join(morpheme)]:
                    if this_idx != idx:
                        new_morphemes = tokens2morphemes(wl[idx,'tokens'])
                        pre_morphemes = ' '.join([' '.join(x) for x in
                            new_morphemes[:pos]])
                        post_morphemes = ' '.join([' '.join(x) for x in
                            new_morphemes[pos+1:]])
                        line = [concept, pre_morphemes, ' '.join(morpheme),
                                post_morphemes]
                        flatlist[i] += [line]

            if max([len(x) for x in flatlist]):
            
                count = 0
                tbl = ''
                flats = []
                for flat in flatlist:
                    flats += ['| concept | preceding | morpheme | following | ']
                flats = ' **——** '.join(flats)
                tbl += flats
                tbl += '\n'
                head = []
                for flat in flatlist:
                    head += ['| --- | --- | --- | --- | ']
                head = '---'.join(head)
                tbl += head
                tbl += '\n'
                for i, flat in enumerate(flatlist):
                    flatlist[i] = sorted(flat, key=lambda x: x[0])
                while count < max([len(x) for x in flatlist]):
                    tbl += ''
                    for flat in flatlist: #, key=lambda x: x[0] if x else 0):
                        try:
                            tbl += '| "{0}" | {1} | **{2}** | {3} | '.format(*flat[count])
                        except IndexError:
                            tbl += '| | | | | '
                    tbl += '\n'
                    count += 1
                txt += tbl
                txt += '\n'
            else:
                txt += ' -- (unique concept) \n\n'
with open('profiles.html', 'w') as f:
    f.write(markdown.markdown(txt, extensions=['markdown.extensions.tables']))
with open('profiles.md', 'w') as f:
    f.write(txt)
