import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from([(1, {"color": "red"}),
                  (2, {"color": "blue"}),
                   (3, {"color": "green"})])
nx.draw(G)
plt.subplot(121)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

plt.show()
