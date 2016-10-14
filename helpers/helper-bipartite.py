from pyburmish.phonology import *
import networkx as nx
from networkx import bipartite as bt
from pyclics.utils import save_network

table, *rest = initials_and_rhymes('Lashi')

G = nx.Graph()
for k, v in table.items():
    G.add_node(' '.join(k), bipartite=0)
    for val, occ in v.items():
        if not val in G.node:
            G.add_node(val, bipartite=1)
        G.add_edge(' '.join(k), val, weight=len(occ))

initials = {n for n, d in G.nodes(data=True) if d['bipartite'] == 1}
finals = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}

I = bt.projection.collaboration_weighted_projected_graph(G, initials)
F = bt.projection.collaboration_weighted_projected_graph(G, finals)

save_network('initials.gml', I)
save_network('finals.gml', F)
save_network('bipartite.gml', G)
