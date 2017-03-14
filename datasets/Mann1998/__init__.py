from lingpy import *
from collections import namedtuple
from collections import defaultdict
from pyconcepticon.api import Concepticon

def prepare(ds):
    cmap = {
            'earth, soil' : 'earth or soil',
            'lime(betel)' : 'lime (betel)',
            'road, path' : 'road or path',
            "under house": "space under house", 
            "full, satisfied" : "full or satisfied",
            "be drunk" : "drunk",
            "lie, fib" : "lie or fib",
            "to itch" : "itch", 
            "go; return" : "return",
            "rub, scrub" : "rub or scrub",
            "burnt (corpse)" : "burned (a corpse)", 
            "pound(rice)" : "pound (rice)",
            "one(person)" : "one (person)",
            "two(ppl)" : "two (people)",
            "three(ppl)" : "three (people)",
            "four(ppl)" : "four (people)",
            "five(ppl)" : "five (people)",
            "six(ppl)" : "six (people)",
            "seven(ppl)" : "seven (people)",
            "eight(ppl)" : "eight (people)",
            "nine(ppl)" : "nine (people)",
            "ten(ppl)" : "ten (people)",
            "hundred(ppl)" : "hundred (people)",
            "thousand(ppl)" : "thousand (people)",
            "many(ppl)": "many (people)",
            "wide, broad" : "wide or broad",
            "spherical" : "round"
            }
    ds.concepts["bark2"] = namedtuple('cset', 'concepticon_id')
    ds.concepts["bark2"].concepticon_id = "1206"

    crect = {
            "dzi⁵² (tusk)/tsɨ̣⁵²(tooth)": "dzi⁵²",
            "-⁵⁴" : ""
            }
    data = defaultdict(lambda : defaultdict(list))
    concepts = []
    # reconstruct the morphemes
    csv = csv2list(ds.raw('Mann-redo.csv'), strip_lines=False)
    header, rest = csv[0], csv[1:]
    for line in rest:
        tmp = dict(zip(header, line))
        concept = tmp['Mann_meaning']
        
        cset = tmp['Mann_number']
        cid = cset[:-1]
        concepts += [(concept, cid)]
        for l, lid in ds.lid2lang.items():
            ipa = tmp[l]
            if crect.get(ipa, ipa):
                data[lid][concept] += [(ipa, cset)]


    D = {0: ['language', 'language_is', 'concept', 'concept_id', 'concepticon_id', 'ipa',
        'cogid_is', 'partial_ids', 'tokens']}
    idx = 1
    renum = {'': 0}
    concepts = sorted(set(concepts), key=lambda x: x[1])
    for concept, cid in concepts:
        cidx = ds.concepts[cmap.get(concept, concept)].concepticon_id
        for language in ds.languages:
            items = data[language][concept]
            if items:
                morphs = [x[0] for x in items]
                cogids_ = [x[1] for x in items]
                cogids = []
                for m in cogids_:
                    if m not in renum:
                        renum[m] = max(renum.values())+1
                    cogids += [renum[m]]
                

                D[idx] = [
                        language, '', concept, cid, cidx, '+'.join(morphs), 
                        ' '.join(cogids_), cogids,
                        ds.profile('+'.join([crect.get(m, m) for m in morphs]),
                            'Segments').split(' ')]
                idx += 1
    wl = Wordlist(D)
    wl.renumber('cogid_is', 'cogid')
    for idx, ipa, segment in iter_rows(wl, 'ipa', 'tokens'):
        if '�' in segment:
            print(idx, ipa, segment)
    wl.output('tsv', filename='test', ignore='all')
    alm = Alignments(wl, ref='partial_ids')
    alm.align(method='progressive')
    ds.write_wordlist(alm)


            
            

