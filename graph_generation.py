#!/usr/bin/env python
# encoding: utf-8

"""
Take a username $id_o and generate a graph with $n nodes starting from $id_o.   
Then write the graph nodes and edges into separated files. 
"""

import tweepy #https://github.com/tweepy/tweepy
import copy

#Twitter API credentials
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

def generate_graph(id_o, n, max_followers=5000):
    """
    Generate a graph with $n nodes starting from $id_o.   
    Don't consider any node that has more than $max_followers followers. 
    """
    #consider only users who have less than $max_followers followers
    #max_followers  = 0.1*n

    #check if the account of $id_o is protected
    followers  = []
    try:
        followers = api.followers_ids(id=id_o)
    except tweepy.TweepError: #protected account  
        print('The account of %s is protected.')
        return [], [], [] 

    #check if the $id_o has more than $max_followers followers
    if len(followers) >= max_followers:                            
        print('User has more than %d followers.'%max_followers)      
        return [], [], []                                               

    #initialize variables
    nodes, levels, edges = [id_o],[[id_o]],[] #$levels are just to split $nodes into layers
    pre_lvl = {id_o:followers}
    next_lvl = {}
    black_list = []

    while len(nodes) < n:
        for id_u, u_followers in pre_lvl.items():
            for id_v in u_followers:
                #if $id_v is already in $nodes, just add the related edge
                if id_v in nodes:
                    edges.append((id_u, id_v))
                    continue

                #skip $id_v if it is on the $black_list: protected account or followers > $max_followers
                if id_v in black_list:
                    continue

                #if there are already $n nodes, then don't add anymore (just complete the for loop while adding the necessary edges)
                if len(nodes) < n:
                #try to get followers of $id_v
                    try:
                        followers = api.followers_ids(id=id_v)
                    except tweepy.TweepError: #protected account  
                        black_list.append(id_v)
                        continue
                    
                    #too many followers, add into the $black_list
                    if len(followers) >= max_followers:
                        black_list.append(id_v)
                        continue
                    
                    #add $id_v to nodes
                    nodes.append(id_v)
                    #add related edge
                    edges.append((id_u, id_v))
                    #add $id_v followers to $next_lvl
                    next_lvl[id_v] = followers

        #if no nodes in $next_lvl, then end the while loop
        if len(next_lvl) == 0:           
            break  

        #obtain the nodes of the current level
        u_lvl = []
        for lvl in levels:
            u_lvl.extend(lvl)
        levels.append(list(set(nodes)-set(u_lvl)))

        pre_lvl = copy.deepcopy(next_lvl)
        next_lvl = {}
        print('Level %d generation ...'%(len(levels)-1))

    #complete the edges of the graph (those from last level)
    print('Complete edges ...')
    for id_u, u_followers in pre_lvl.items():
        for id_v in u_followers:
            if id_v in nodes:
                edges.append((id_u, id_v))
    return nodes, levels, edges

USR_NAME =  'alevalerossi' #screen_name (str) or id (int)
NB_NODES = 10
MAX_FOLLOWERS = 1000
if __name__ == '__main__':

	#authentication
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)

	#get id from user_name
	if isinstance(USR_NAME, str):
		id_o = api.get_user(USR_NAME).id

	#generate graph starting from user $id_o
	nodes, levels, edges = generate_graph(id_o, n=NB_NODES, max_followers=MAX_FOLLOWERS)
	print('Number of levels is %d: '%len(levels))

	#write nodes into a file
	f = open('%s_graph_nodes'%USR_NAME, 'wb') 
	f.write('\n'.join(str(x) for x in nodes))
	f.close()

	#write edges into a file
	f = open('%s_graph_edges'%USR_NAME, 'wb') 
	f.write('\n'.join(str(x) + ' ' + str(y) for (x, y) in edges))
	f.close()

	#write levels into files
	for i, lvl in enumerate(levels): 
		f = open('%s_graph_level_%d'%(USR_NAME, i), 'wb') 
		f.write('\n'.join(str(x) for x in lvl))
		f.close()

	print('Done!')
