#!/usr/bin/env python
# encoding: utf-8

"""
Optimize graph by removing nodes with "low degree".
"""


def remove_node(id_u, nodes, edges, levels, k):
	"""
	Remove node $id_u from the graph. 
	"""
	nodes.remove(id_u)
	levels[k].remove(id_u)
	for (x, y) in edges:
		if x == id_u or y == id_u:
			edges.remove((x,y))
	return 


def get_outgoing_edges_number(id_u, edges):
	"""
	Get the number of outgoing edges from $id_u.
	"""
	edges_nb = 0
	for (x,y) in edges:
		if x == id_u:
			edges_nb += 1
	return edges_nb 


def get_edges_number(id_u, edges):
	"""
	Get the number of (outgoing and ingoing) edges from $id_u.
	"""
	edges_nb = 0
	for (x,y) in edges:
		if x == id_u or y == id_u:
			edges_nb += 1
	return edges_nb 


def optimize_graph(nodes, levels, edges, max_nodes):
	"""
	Optimize graph and keep only $max_nodes nodes. 
	"""
	#remove nodes with 0 outgoing edges
	for lvl in reversed(levels):
		for id_u in lvl:
			if len(nodes) <= max_nodes:
				return 
			if get_outgoing_edges_number(id_u, edges) == 0:
				remove_node(id_u, nodes, edges, levels, levels.index(lvl))

	#recursively remove the node with minimal number of edges until reaching $max_nodes
	while(len(nodes) > max_nodes):
		min_edges_nb = get_edges_number(nodes[0], edges) #initial value
		id_m = nodes[0] #initial value
		for id_u in nodes:
			edges_nb = get_edges_number(id_u, edges)
			if  edges_nb < min_edges_nb:
				min_edges_nb = edges_nb
				id_m = id_u

		#get level number
		for i, lvl in enumerate(levels):
			if id_m in lvl:
				break
		#remove node
		remove_node(id_m, nodes, edges, levels, i)
	return 


def read_graph(usr_name, levels_nb):
	#read nodes from a file
	nodes = []
	f = open('%s_graph_nodes'%usr_name, 'r')
	for line in f:
		nodes.append(int(line))
	f.close()

	#read edges from a file
	edges = []
	f = open('%s_graph_edges'%usr_name, 'r')
	for line in f:
		line = line.split(' ')
		edges.append((int(line[0]), int(line[1])))
	f.close()

	#read levels from  files
	levels = []
	for i in range(levels_nb): 
		lvl = []
		f = open('%s_graph_level_%d'%(usr_name, i), 'r')
		for line in f:
			lvl.append(int(line))
		f.close()
		levels.append(lvl)
	return nodes, levels, edges


def write_graph(usr_name, nodes, levels, edges):

	#write nodes into a file
	f = open('%s_opt_graph_nodes'%usr_name, 'wb') 
	f.write('\n'.join(str(x) for x in nodes))
	f.close()

	#write edges into a file
	f = open('%s_opt_graph_edges'%usr_name, 'wb') 
	f.write('\n'.join(str(x) + ' ' + str(y) for (x, y) in edges))
	f.close()

	#write levels into files
	for i, lvl in enumerate(levels): 
		f = open('%s_opt_graph_level_%d'%(usr_name, i), 'wb') 
		f.write('\n'.join(str(x) for x in lvl))
		f.close()

	return


USR_NAME =  
LVL_NB = 

if __name__ == '__main__':

	nodes, levels, edges = read_graph(USR_NAME, LVL_NB)
	optimize_graph(nodes, levels, edges, 3)
	write_graph(USR_NAME, nodes, levels, edges)
	print('Done!')

