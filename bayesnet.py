from __future__ import division
from collections import OrderedDict
import numpy as np 
import pandas as pd 
import time


__author__ = "Navreet Kaur"
__entrynumber__ = "2015TT10917"


class Graph_Node():
	"""Our graph consists of a list of nodes where each node is represented as follows"""

	def __init__(self, name, n, vals):
		self.Node_Name = name # Variable name 
		self.nvalues = n # Number of categories a variable represented by this node can take
		self.values = vals # Categories of possible values
		self.Children =  [] # Children of a particular node - these are index of nodes in graph.
		self.Parents = [] # Parents of a particular node- note these are names of parents
		self.CPT = []
		self.cpt_data =  pd.DataFrame() # conditional probability table as a DataFrame (counts) 
		self.markov_blanket = [] # List of nodes in the Markov Blanket - note that these are the names of the nodes

	def get_name(self):
		return self.Node_Name

	def get_children(self):
		return self.Children

	def get_Parents(self):
		return self.Parents

	def get_n_parents(self):
		return len(self.Parents)

	def get_CPT(self):
		return self.CPT

	def get_nvalues(self):
		return self.nvalues

	def get_values(self):
		return self.values

	def set_CPT(self, new_CPT):
		del(self.CPT[:])
		self.CPT = new_CPT

	def set_counts(self, new_counts):
		del(self.counts[:])
		self.counts = new_counts

	def set_MB(self, new_mb):
		self.markov_blanket = new_mb

	def set_cpt_data(self, new_cpt_data):
		self.cpt_data.drop(columns = list(self.cpt_data.columns))
		self.cpt_data = new_cpt_data

	def set_Parents(self, Parent_Nodes):
		self.Parents = Parent_Nodes

	def add_child(self, new_child_index):
		if new_child_index in self.Children:
			return 0
		else:
			self.Children.append(new_child_index)
			return 1

	def print_node(self):
		print(self.Node_Name)
		print(self.values)
		print(self.Parents)
		print(self.CPT)
		print


class network():
	"""
	The whole network represted as a dictionary of nodes
	Pres_Graph: 
		Ordered Dictionary - Keys: variable names, Values: Node Objects
	MB:
		Ordered Dictionary - Keys: variable names, Values: List of names of the nodes in the markob blanket of the key
	"""

	def __init__(self, Pres_Graph = OrderedDict(), MB = OrderedDict()):
		self.Pres_Graph = Pres_Graph
		self.MB = MB

	def addNode(self, node):
		self.Pres_Graph[node.Node_Name] = node

	def netSize(self):
		return len(self.Pres_Graph)
		
	def get_index(self, val_name):
		try:
			return self.Pres_Graph.keys().index(val_name)
		except:
			print "No node of the name: " + str(val_name)
			return None

	def get_nth_node(self, n):
		return self.Pres_Graph.values()[n]

	def search_node(self, val_name):
		try:
			return self.Pres_Graph[val_name]
		except:
			print "Node NOT found"
			return None

	def get_parent_nodes(self, node):
		parent_nodes = []
		parents = node.get_Parents()
		for p in parents:
			parent_nodes.append(self.search_node(p))
		return parent_nodes

	def get_children(self, val_name):
		Children = self.Pres_Graph[val_name].Children
		c = []
		for n in Children:
			c.append(self.Pres_Graph.keys()[n])
		return c

	def set_mb(self):
		for vals in self.Pres_Graph.keys():
			self.MB[vals] = markov_blanket(self, vals)
			

	def normalise_cpt(self, X):
		l = [X] + self.Pres_Graph[X].Parents + ['counts', 'p']
		cpt = self.Pres_Graph[X].cpt_data
		nvals = self.Pres_Graph[X].nvalues
		cardinality = cpt.shape[0]
		no_grps = int(cardinality/nvals)
		list_dfs = []
		df = pd.DataFrame()
		i=0 
		for n in range(no_grps):
			curr_df = pd.DataFrame(cpt.iloc[i:i+nvals, :])
			curr_df['p'] = normalise_counts(curr_df['counts'])
			df = df.append(curr_df)
			i = i + nvals
		self.Pres_Graph[X].cpt_data = df[l]


""" Reading network from .bif format """
def read_network(bif_filepath):
	Alarm = network()
	find = 0

	with open(bif_filepath, 'r') as  myfile: 
		while True:
			line = myfile.readline()
			line = line.strip()

			if line == '':
				break

			tokens = line.split()
			first_word = tokens[0]


			if first_word == "variable":
				values = []
				name = tokens[1] # random varible name
				line_ = myfile.readline() # read next line
				line_ = line_.strip()
				tokens_ = line_.split()
				for i in range(3,len(tokens_)-1):
					values.append(tokens_[i])
				new_node = Graph_Node(name = name, n = len(values), vals = values)
				Alarm.addNode(new_node)

			
			if first_word == "probability":
				vals = []
				temp = tokens[2]
				node = Alarm.search_node(temp)
				index = Alarm.get_index(temp)
				i = 3
				# setting parents
				while True:
					if tokens[i]==")":
						break
					node_ = Alarm.search_node(tokens[i])
					node_.add_child(index)
					vals.append(tokens[i])
				 	i = i + 1

				node.set_Parents(vals)

				line_ = myfile.readline()
				tokens_ = line_.split()
				curr_CPT = []
				for i in range(1,len(tokens_)-1):
					curr_CPT.append(int(tokens_[i]))

				node.set_CPT(curr_CPT)

	myfile.close()

	return Alarm


# Get variables in the markov blanket of variable 'val_name' 
def markov_blanket(net, val_name):
	node = net.search_node(val_name)
	mb = []
	# Parents
	parents = node.Parents
	mb = mb + parents
	# Children
	children_names = node.Children
	for c in children_names:
		child_node = net.Pres_Graph[net.Pres_Graph.keys()[c]]
		mb.append(child_node.Node_Name)
		# Spouses
		spouses = child_node.Parents
		for var in spouses:
			if var not in mb and var!=val_name:
				mb.append(var)

	return mb


# Get the datafile as a pandas dataframe 
def get_data(filepath):
	with open(filepath,'r') as f:
		df = pd.DataFrame(l.rstrip().split() for l in f)

	df.columns = ['"Hypovolemia"','"StrokeVolume"','"LVFailure"','"LVEDVolume"','"PCWP"','"CVP"','"History"',
	'"MinVolSet"','"VentMach"','"Disconnect"','"VentTube"','"KinkedTube"','"Press"','"ErrLowOutput"',
	'"HRBP"','"ErrCauter"','"HREKG"','"HRSat"','"BP"','"CO"','"HR"','"TPR"','"Anaphylaxis"','"InsuffAnesth"','"PAP"','"PulmEmbolus"',
	'"FiO2"','"Catechol"','"SaO2"','"Shunt"','"PVSat"','"MinVol"','"ExpCO2"','"ArtCO2"','"VentAlv"','"VentLung"','"Intubation"']

	features = list(df.columns)

	mapping_1 = {'"True"': 0, '"False"': 1, '"?"': float('nan')}
	mapping_2 = {'"Zero"': 0, '"Low"': 1, '"Normal"': 2, '"High"': 3, '"?"': float('nan')}
	mapping_3 = { '"Normal"': 0, '"Esophageal"': 1 , '"OneSided"': 2, '"?"': float('nan') }
	mapping_4 = {'"Low"':0, '"Normal"':1, '"High"':2, '"?"': float('nan')}
	mapping_5 = {'"Low"':0, '"Normal"':1, '"?"': float('nan')}
	mapping_6 = {'"Normal"':0, '"High"':1, '"?"': float('nan')}
	overall_mapping = { '"Hypovolemia"':mapping_1 , u'"StrokeVolume"':mapping_4, u'"LVFailure"':mapping_1, 
	                   u'"LVEDVolume"':mapping_4, u'"PCWP"':mapping_4, u'"CVP"':mapping_4, 
	                   u'"History"':mapping_1, u'"MinVolSet"':mapping_4, u'"VentMach"':mapping_2, u'"Disconnect"':mapping_1,
	                   u'"VentTube"':mapping_2, u'"KinkedTube"':mapping_1, u'"Press"':mapping_2, 
	                   u'"ErrLowOutput"':mapping_1, u'"HRBP"':mapping_4,
	                   u'"ErrCauter"':mapping_1, u'"HREKG"':mapping_4, u'"HRSat"':mapping_4, 
	                   u'"BP"':mapping_4, u'"CO"':mapping_4, u'"HR"':mapping_4, u'"TPR"':mapping_4,
	                   u'"Anaphylaxis"':mapping_1, u'"InsuffAnesth"':mapping_1, u'"PAP"':mapping_4, 
	                   u'"PulmEmbolus"':mapping_1, u'"FiO2"':mapping_5,
	                   u'"Catechol"':mapping_6, u'"SaO2"':mapping_4, u'"Shunt"':mapping_6, 
	                   u'"PVSat"':mapping_4, u'"MinVol"':mapping_2, u'"ExpCO2"':mapping_2,
	                   u'"ArtCO2"':mapping_4, u'"VentAlv"':mapping_2, u'"VentLung"':mapping_2, u'"Intubation"':mapping_3}
	df = df.replace(overall_mapping)
	# to get csv file of data
	# df.to_csv('records.csv')
	return df


# normalise a list of counts
def normalise_counts(vals):
	vals[vals==0] = 0.000005
	denom = np.sum(vals)
	normalised_vals = []
	for val in vals:
		normalised_vals.append(val/float(denom))
	return normalised_vals


if __name__ == '__main__':
	print "This file contains Bayes Net classes: Run main.py"
