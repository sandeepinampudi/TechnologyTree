import collections
import math
def branchplot(child_techs,x0,y0,pos,parent_tech,G,scl,data):
    '''
    This recursive funtion perform level-by-level 
    updates the pameters required to make the network/tree plot.
    x0,y0 : coordinates of the parent node
    pos : coordinates of all nodes    
    scl : scaling factor  for lower levels 
    '''
    x = x0 - scl*(len(child_techs)-1)/2 # horizontal position
    for name in child_techs:        
        G.add_edge(parent_tech,name)              
        if name not in pos:           
            pos[name] = (x, math.log10(data[name]['total_patents']))
            x+=scl          
        if isinstance(child_techs[name], collections.MutableMapping):
           scl = 0.50*scl    
           pos, scl, G = branchplot(child_techs[name], pos[name][0], pos[name][1], pos, name, G, scl, data)
           scl = 1
    return pos, scl, G
