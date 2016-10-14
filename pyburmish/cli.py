from pyburmish import *
from pyburmish.phonology import *
from pyburmish.patterns import *
from pyburmish.colexification import *

def main():
    from sys import argv
    target, limit, variety, pattern, verbose = 'url', 10, None, 'A', False
    if '-t' in argv:
        target = argv[argv.index('-t')+1]
    if '-l' in argv:
        limit = int(argv[argv.index('-l')+1])
    if '-v' in argv:
        variety = argv[argv.index('-v')+1]
    if '-p' in argv:
        pattern = argv[argv.index('-p')+1]
    if '--verbose' in argv:
        verbose = True

    if 'backup' in argv:
        backup(target)
    if 'download' in argv:
        download(target)
    if 'history' in argv:
        history(limit)
    if 'coverage' in argv:
        language_coverage()
    if 'check' in argv:
        check_burmish()
    if 'rhymes' in argv:
        table, initials, medials, nuclei, finals, tones = initials_and_rhymes(variety)
        print(format_the_table(table, initials, medials, nuclei, finals, tones))
    if 'articulation_points' in argv:
        graph, aps = articulation_points(
                make_bipartite(
                    initials_and_rhymes(variety)[0]))
        for p in sorted(set(aps), 
                key=lambda x: (len(x.split(' ')), x)):
            print(p, graph.node[p]['occ'])
    if 'make' in argv:
        if 'alignments' in argv:
            make_alignments(verbose=verbose)
    if 'patterns' in argv:
        alms = get_alignments()
        G, cliques = strict_compatibility_graph(alms, ref='pcogids',
                pos=pattern, mintax=3, verbose=verbose)
        if 'extract' in argv:
            text = '\t'.join(['No.', 'Context', 'Frequency', 'Concepts',
                'Cognates']+["Old_Burmese", "Burmese", "Written_Burmese",
        "Rangoon", "Achang_Longchuan", "Xiandao", "Lashi", "Atsi", "Bola", "Maru"])
            text += '\n'
            for line in extract_patterns(alms, G, pattern, ref='pcogids',
                    verbose=verbose):
                text += '\t'.join(['{0}'.format(x) for x in line])+'\n'
            with open('patterns-{0}.tsv'.format(pattern), 'w') as f:
                f.write(text)
        if 'collapsible' in argv:
            collapsible_patterns(alms, G, pattern)
        if 'html' in argv:
            cgraph_to_html(alms, G, pattern, cliques, verbose=True, ref='pcogids')
    if 'check' in argv:
        if 'phonology' in argv:
            print(format_phonostats(phonostats()))
    if 'colexification' in argv:
        if 'bipartite' in argv:
            compare_partial_colexifications()

