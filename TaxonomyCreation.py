import json
import networkx as nx
import matplotlib.pyplot as plt
from definitions import TreeMaker
from GraphPlots import branchplot
import csv

# load the data
#input_file=open('validation_techs.json', 'r')
input_file=open('top_100_techs.json', 'r')

data00=json.load(input_file)
data=dict()
for dt in data00:
    data[dt['technology']]={'ipc_codes' : dt['ipc_codes'],'total_patents' : dt['total_patents']}

# Assign Relationships
Tech_names=list(data.keys())
TreeLst={'STEM' : Tech_names}
ConnTechEdges={}
TreeLst,ConnTechEdges,lim=TreeMaker(TreeLst,data,ConnTechEdges,0.50)
print(TreeLst)

## Graph creation     
G=nx.DiGraph()
labels={}
pos=dict()

# manual insetion of super parent node 
G.add_node('STEM')
labels['STEM']='STEM'
x0,y0=0,7
pos['STEM']=(x0,y0)

# Nodes 
G.add_nodes_from(Tech_names)
for tech in Tech_names:   
    labels[tech]=tech

#Edges
G.add_edges_from(list(ConnTechEdges.keys()))
for tech in TreeLst:
    pos,scl,G=branchplot(TreeLst[tech],x0,y0,pos,tech,G,1,data) 

#Edge Colors
edgecolors=[]
for edge in G.edges():
    if edge in ConnTechEdges:       
       edgecolors.append([0.9,0.9,0.9])
    else:
       edgecolors.append([0,0,0])

# plotting
plt.figure(figsize=(30,8))
nx.draw_networkx_nodes(G, pos, node_size=400,node_shape='s', nodelist=list(pos.keys()),with_labels=True)
nx.draw_networkx_edges(G, pos, alpha=1, width=2,edge_color=edgecolors)
nx.draw_networkx_labels(G,pos,labels,font_size=17)
plt.ylabel('log(Total Patents)', fontsize=20) 
plt.xlim(-4,4)
plt.yticks(fontsize=20)

# csv file prepapration for rawgraphics webapp
G2 = G
G2.remove_edges_from(list(ConnTechEdges.keys()))
tail_list = [x for x in G2.nodes() if G2.out_degree(x) == 0 and G2.in_degree(x) == 1]

paths = []
n_lev = 0
for tech in tail_list:
    for path in nx.all_simple_paths(G2, source = 'STEM', target = tech):    
        n_lev = max(n_lev,len(path))
        paths.append(path)
        
header=['Level '+str(j) for j in range(n_lev)]

with open('tree_graphics.csv', 'w') as csvFile:
     writer = csv.writer(csvFile,delimiter=',', lineterminator='\n')
     writer.writerow(header)
     for path in paths:
         writer.writerow(path)
csvFile.close()