import collections

def TreeMaker(TreeLst,data,EdgeDict,lim):
    '''
    This recursive funtion is the main body.
    It builds the tree level-by-level repetedly calling itself
    The input and output dict TreeLst represent a dictionay of dictionaries
    data : the source dictionary with ipcodes, percentages, and total patents  
    lim : threshold to classify connected  or not-connected
    EdgeDict : A dictionary of pairs of connected edges
    '''
    
    for techs in TreeLst:
        TreeDict, EdgeDict, lim = assign_relations(TreeLst[techs], data, EdgeDict, lim)
        TreeLst[techs] = TreeDict
        lim = lim - 0.1 # threshold adjustment at each level
        if isinstance(TreeLst[techs], collections.MutableMapping): # ready for the next level
            TreeMaker(TreeLst[techs], data, EdgeDict, lim) 
    return TreeLst, EdgeDict, lim

def assign_relations(Tech_names, data, EdgeDict, lim):
    ''' 
    This function performs one level of clustering into gropus and classifying into
    parent-child/connected/not connected relations between techs in Tech_names
    '''
    Tech_names = sorted(Tech_names, key=lambda k: -data[k]['total_patents'])
    TreeDict = dict()
    parent_techs = []
    for tech2 in Tech_names:
        
        # calculate pattern match quantities with parents
        patt_match_coeff, tot_pat_rat = calc_pattern_match(data[tech2], parent_techs,data)
        
        # find relationships with existing parents
        relations, EdgeDict = find_relations(patt_match_coeff, tot_pat_rat, 
                                             parent_techs,lim,EdgeDict,tech2)
        # update the tree 
        TreeDict, parent_techs = tree_update(relations, TreeDict, parent_techs, tech2)       

    return TreeDict, EdgeDict, lim

def calc_pattern_match(chld, parents,data):
    '''
    This function returns pattern match factor and total patent ratios of a child with 
    respect to a set of parents 
    '''
    patt_match_coeff, tot_pat_rat= [], []
    for tech in parents:
        parent=data[tech]
        Ip,p1,p2 = get_IP_codes(parent['ipc_codes'],chld['ipc_codes'])
        patt_match_coeff.append(sum([abs((p2_0-p1_0)/(p2_0+p1_0))**2 for p1_0,p2_0 in zip(p1,p2)])/40)
        tot_pat_rat.append(chld['total_patents']/parent['total_patents'])
    
    return patt_match_coeff, tot_pat_rat

def find_relations(patt_match_coeff, tot_pat_rat, parent_techs,lim,EdgeDict,chld):
    '''
    This function assigns and returns the relations (Not Connected, parent-child, or Connected )
    based on pattern match factors. 
    lim : represent threshold between connected and not connected 
    '''
    relations = [] # Not Connected, parent-child, or Connected 
    for g, p, par in zip(patt_match_coeff, tot_pat_rat, parent_techs):
        if g >= lim: # Un-matched patent pattern  
            relations.append('NC') # Not Connected
        else: 
            if (g == min(patt_match_coeff)) and p < 0.5: #parent-child
                relations.append('PC')
            else: # Siblings
                relations.append('C')
                EdgeDict[(chld,par)] = 'Connected Tech'
                EdgeDict[(par,chld)] = 'Connected Tech'
        
    return relations, EdgeDict 
    
def tree_update(relations, TreeDict, parent_techs, chld):
    '''
    This function updates the tree based on given relationships 
    '''
    if 'PC' not in relations: 
        parent_techs.append(chld)
        TreeDict[chld] = []
    else:
        parent = parent_techs[relations.index('PC')]
        if parent in TreeDict: 
           TreeDict[parent].append(chld)            
        else:
           TreeDict[parent] = chld
    
    return TreeDict, parent_techs

def get_IP_codes(T1, T2):
    '''
    This function returns a unioun of Ipc Codes and their percentages
    for input Tech dictionaries T1 and T2. 
    '''
    # code collection
    Ipcs_T1 = [j['ipc_code'] for j in T1]
    Ipcs_T2 = [j['ipc_code'] for j in T2]    
    
    # code union
    Ipcs_union = list(set().union(Ipcs_T1,Ipcs_T2))
     
    # ratio collection for union set
    Ipcs_rat_T1, Ipcs_rat_T2 = [], []
    for Ip in Ipcs_union:
        p1, p2 = 0, 0
        if Ip in Ipcs_T1:
           p1 = T1[Ipcs_T1.index(Ip)]['percentage']
        if Ip in Ipcs_T2:
           p2 = T2[Ipcs_T2.index(Ip)]['percentage']  
        
        Ipcs_rat_T1.append(p1)
        Ipcs_rat_T2.append(p2)   
    
    return Ipcs_union, Ipcs_rat_T1, Ipcs_rat_T2
