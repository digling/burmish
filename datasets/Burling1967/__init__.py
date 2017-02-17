from lingpy import *
from lingpy.sequence.sound_classes import syllabify

def prepare(ds):
    
    rawdata = csv2list(ds.raw('Burling1967.csv'), strip_lines=False)

    concepts = []
    header = rawdata[0]
    crect = {}
    D = {0: [
        'doculect',
        'concept',
        'doculect_is',
        'concept_number_is',
        'value_is',
        'value',
        'notes',
        'notes_mm',
        'cogid',
        'segments'
        ]}
    idx = 1
    cogid = 1
    for i, line in enumerate(rawdata[1:]):
        tmp = dict(zip(header, line))
        concepts += [(tmp['number'], tmp['meaning'])]
        for lid, lang in sorted(ds.lid2lang.items()):
            cell = tmp[lid]
            if cell.strip() != '-' and cell.strip():
                ccell = crect.get(cell, cell)
                syls = ' + '.join([' '.join(x) for x in syllabify(
                    ccell, output='nested')])
                D[idx] = [
                        lang, tmp['meaning'], lid, tmp['number'], cell,
                        ccell, tmp['notes'], tmp['MM notes'], 
                        cogid, syls]
                idx += 1
        cogid += 1
    with open(ds.raw('concepts.tsv'), 'w') as f:
        f.write('NUMBER\tENGLISH\n')
        for a, b in concepts:
            f.write(a+'\t'+b+'\n')
    ds.write_wordlist(Wordlist(D))
