from lingpy import *

burmish = csv2list('../tsv/burmish.concepts.tsv')
stdb = csv2list('../tsv/STDB-2016-250.tsv')


# get code for tbl
stdb_tbl = dict([(line[3].rjust(4,'0'), (line[0], line[1], line[4])) for line in stdb[1:]])
brm_tbl = dict([(line[-1].rjust(4,'0'), (line[0], line[1])) for line in burmish])
new_burmish = []
for key,val in stdb_tbl.items():
    if key in brm_tbl:
        new_burmish += [[val[0], val[1], brm_tbl[key][1], val[2], key]]
    else:
        new_burmish += [[val[0], val[1], '???', val[2], key]]

# get missing in tbl
with open('burmish.new.concepts.tsv', 'w') as f:
    f.write("STDB_ID\tSTDB_GLOSS\tBURMISH_GLOSS\tCONCEPTICON_ID\tTBL_ID\n")
    for line in sorted(new_burmish, key=lambda x: int(x[0])):
        f.write('\t'.join(line)+'\n')

