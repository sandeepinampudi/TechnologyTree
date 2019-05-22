import json
import networkx as nx
import matplotlib.pyplot as plt
from definitions import TreeMaker
from GraphPlots import branchplot

# load the data
input_file=open('validation_techs.json', 'r')
#input_file=open('top_100_techs.json', 'r')

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

for tech in TreeLst:
    for tech2 in TreeLst[tech]:
        for tech3 in TreeLst[tech][tech2]:        
            print(tech, tech2, tech3)

