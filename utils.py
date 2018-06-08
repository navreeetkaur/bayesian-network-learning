from __future__ import division
from bayesnet import Graph_Node, network
import bayesnet
import numpy as np 
import pandas as pd 
import time
from collections import OrderedDict

# Setup the network
def setup_network(bif_alarm, dat_records):
	# Parsing the network from .bif format 
	print "0: Reading Network . . . "
	Alarm = bayesnet.read_network(bif_alarm)
	# Finding markov blanket for every
	print "1: Setting Markov Blankets . . . "
	Alarm.set_mb()
	# Get data from record.dat
	print "2: Getting data from records . . . "
	df = bayesnet.get_data(dat_records)
	# Initialise parameters
	print "3: Initialising parameters . . . "
	init_params(df, Alarm)
	# Get the index of nodes which have missing value in each row
	print "4: Getting missing data indexes . . . "
	mis_index = get_missing_index(df)
	return Alarm, df, mis_index

# List of the indices of nodes which have missing values in each data point; 
# equal to -1 if no value is missing
def get_missing_index(df):
	mis_index = []
	for index, row in df.iterrows():
	    if(row.isnull().any()):
	        mis_index.append(int(np.argwhere(np.isnan(np.asarray(row)))))
	    else:
	    	mis_index.append(-1)
	return mis_index

# Initialise parameters
def init_params(df, net):
	N = df.shape[0]
	curr_iter = 0
	for node in net.Pres_Graph.values():
		parents = net.get_parent_nodes(node)
		n_parents = len(parents)
		if n_parents==0:
			v0 = [] # value of node variable
			counts = []
			for p0 in range(0,node.nvalues):
				a = df[node.Node_Name]==p0
				counts.append(pd.DataFrame(df[a]).shape[0] + 1)
				# counts.append(0.01)
				v0.append(p0)
			cpt_df = pd.DataFrame({node.Node_Name:v0, "p": np.ones(len(counts))*(-1), "counts": counts})
			node.set_cpt_data(cpt_df)

		elif n_parents==1:
			v0 = [] # value of parent1 variable
			v1 = [] # value of node variable
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,node.nvalues):
					b = df[node.Node_Name]==p1
					counts.append(pd.DataFrame(df[a & b]).shape[0] + 1)
					# counts.append(0.01)
					v0.append(p0)
					v1.append(p1)
			cpt_df = pd.DataFrame({node.Node_Name:v1, parents[0].Node_Name:v0 , 
									"p": np.ones(len(counts))*(-1), "counts": counts})
			node.set_cpt_data(cpt_df)
			
		elif n_parents==2:
			v0 = [] # value of node variable
			v1 = [] # value of parent1 variable
			v2 = [] # value of parent2 variable
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,node.nvalues):
						c = df[node.Node_Name]==p2
						counts.append(pd.DataFrame(df[a & b & c]).shape[0] + 1)
						# counts.append(0.01)
						v0.append(p0)
						v1.append(p1)
						v2.append(p2)
			cpt_df = pd.DataFrame({parents[0].Node_Name:v0 ,parents[1].Node_Name:v1, node.Node_Name:v2, 
									"p": np.ones(len(counts))*(-1), "counts": counts})
			node.set_cpt_data(cpt_df)       

		elif n_parents==3:
			v0 = [] # value of node variable
			v1 = [] # value of parent1 variable
			v2 = [] # value of parent2 variable
			v3 = [] # value of parent3 variable
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,parents[2].nvalues):
						c = df[parents[2].Node_Name]==p2
						for p3 in range(0,node.nvalues):
							d = df[node.Node_Name]==p3
							counts.append(pd.DataFrame(df[a & b & c & d]).shape[0] + 1)
							# counts.append(0.01)
							v0.append(p0)
							v1.append(p1)
							v2.append(p2)
							v3.append(p3)
			cpt_df = pd.DataFrame({parents[0].Node_Name:v0 ,parents[1].Node_Name:v1, parents[2].Node_Name:v2,
						node.Node_Name:v3, "p": np.ones(len(counts))*(-1), "counts": counts})
			node.set_cpt_data(cpt_df)

		elif n_parents==4:
			v0 = [] # value of node variable
			v1 = [] # value of parent1 variable
			v2 = [] # value of parent2 variable
			v3 = [] # value of parent3 variable
			v4 = [] # value of parent4 variable
			counts = [] # number of times the same data point is occuring
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,parents[2].nvalues):
						c = df[parents[2].Node_Name]==p2
						for p3 in range(0,parents[3].nvalues):
							d = df[parents[3].Node_Name]==p3
							for p4 in range(0,node.nvalues):
								e = df[node.Node_Name]==p4
								counts.append(pd.DataFrame(df[a & b & c & d & e]).shape[0] + 1)
								# counts.append(0.01)
								v0.append(p0)
								v1.append(p1)
								v2.append(p2)
								v3.append(p3)
								v4.append(p4)
			
			cpt_df = pd.DataFrame({parents[0].Node_Name:v0 ,parents[1].Node_Name:v1, parents[2].Node_Name:v2 ,
				parents[3].Node_Name:v3, node.Node_Name:v4, "p": np.ones(len(counts))*(-1), "counts": counts})
			node.set_cpt_data(cpt_df)

		curr_iter += 1

	for X in net.Pres_Graph.keys():
		net.normalise_cpt(X)

# Normalise a numpy array
def normalise_array(vals):
	denom = np.sum(vals)
	normalised_vals = []
	for val in vals:
		normalised_vals.append(val/float(denom))
	return normalised_vals

# return the rows of the factor table with assignments as specified in E
def get_assignment_for(factor, E, nval):
	curr_factor = factor
	for key, value in E.items():
		if key in list(factor.columns):
			condition = curr_factor[key] == value
			curr_factor = curr_factor[condition]
		if curr_factor.shape[0] == nval:
			return curr_factor
	return curr_factor

# Inference by Markov Blanket Sampling
def markov_blanket_sampling(X, E, bn):
	dist_X = []
	children = bn.Pres_Graph[X].Children
	parents = bn.Pres_Graph[X].Parents
	x_cpt = bn.Pres_Graph[X].cpt_data
	fac_x = get_assignment_for(x_cpt, E, bn.Pres_Graph[X].nvalues)
	fac_c = np.log(np.asarray(fac_x['p']))
	for c in children:
		c_cpt = bn.Pres_Graph[bn.Pres_Graph.keys()[c]].cpt_data
		temp = get_assignment_for(c_cpt, E, bn.Pres_Graph[X].nvalues)
		# fac_c = fac_c*np.asarray(temp['p'])
		fac_c = fac_c + np.log(np.asarray(temp['p']))
	return normalise_array(np.exp(fac_c))

# Expectation Step
def Expectation(bn, df, mis_index):
	"""
	Input: 
		bn - Bayesian Network
		df - Data table
		mis_index - array of missing indices corresponding to the Data table 'df'
	Output:
		new_df - each missing value in a row replaced by the possible values variable can take 
		new_weights - array of weights assigned to each data point
	"""
	new_weights = []
	mydict = df.to_dict(orient = 'records')
	new_df = pd.DataFrame()
	# new_df_list = []
	for i in range(df.shape[0]):
		row = pd.DataFrame(df.loc[i,]).T
		if mis_index[i]!=-1:
			X = bn.Pres_Graph.keys()[mis_index[i]]
			mb_x = bn.MB[X]
			# print "------------------------------------ " + str(i) + "  ------------------------------------"
			# print "------------------------------------ "   + X +    "  ------------------------------------"
			E = {key:value for key, value in mydict[i].items() if (key!=X and key in mb_x)}
			dist_X = markov_blanket_sampling(X, E, bn)
			for n in range(bn.Pres_Graph[X].nvalues):
				row.iloc[0, bn.Pres_Graph.keys().index(X)] = n
				new_weights.append(dist_X[n])
				new_df = pd.concat([new_df, row])
				# new_df_list.append(row)
		# if there is no missing value
		else:
			new_weights.append(1.0)
			new_df = pd.concat([new_df, row])

	return new_weights, new_df

# Maximisation Step
def Maximisation(df, net, weights):
	"""
	Updates the CPTs of all the nodes based on data given weight of each data point
	Input:
		df - Data Table
		net - Bayesian Net
		Weights - weight corresponding to each data point in the table
	Output:
		None
	"""
	df['wts'] = weights
	N = df.shape[0] 
	curr_iter = 0
	for X, node in net.Pres_Graph.items():
		# print "--------- " + X + " ----------"
		parents = net.get_parent_nodes(node)
		n_parents = len(parents)
		if n_parents==0:
			counts = []
			for p0 in range(0,node.nvalues):
				a = df[node.Node_Name]==p0
				count = float(pd.DataFrame(df[a])['wts'].sum())
				if count!=0:
					counts.append(float(count))
				else:
					counts.append(0.000005)
			node.cpt_data['counts'] = counts
			net.normalise_cpt(X)

		elif n_parents==1:
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,node.nvalues):
					b = df[node.Node_Name]==p1
					count = float(pd.DataFrame(df[a & b])['wts'].sum())
					if count!=0:
						counts.append(float(count))
					else:
						counts.append(0.000005)
			node.cpt_data['counts'] = counts
			net.normalise_cpt(X)

		elif n_parents==2:
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,node.nvalues):
						c = df[node.Node_Name]==p2
						count = float(pd.DataFrame(df[a & b & c])['wts'].sum())
						if count!=0:	
							counts.append(count)
						else:
							counts.append(0.000005)
			node.cpt_data['counts'] = counts
			net.normalise_cpt(X)

		elif n_parents==3:
			counts = []
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,parents[2].nvalues):
						c = df[parents[2].Node_Name]==p2
						for p3 in range(0,node.nvalues):
							d = df[node.Node_Name]==p3
							count = float(pd.DataFrame(df[a & b & c & d])['wts'].sum())
							if count!=0:
								counts.append(float(count))
							else:
								counts.append(0.000005)
			node.cpt_data['counts'] = counts
			net.normalise_cpt(X)

		elif n_parents==4:
			counts = [] 
			for p0 in range(0,parents[0].nvalues):
				a = df[parents[0].Node_Name]==p0
				for p1 in range(0,parents[1].nvalues):
					b = df[parents[1].Node_Name]==p1
					for p2 in range(0,parents[2].nvalues):
						c = df[parents[2].Node_Name]==p2
						for p3 in range(0,parents[3].nvalues):
							d = df[parents[3].Node_Name]==p3
							for p4 in range(0,node.nvalues):
								e = df[node.Node_Name]==p4
								count =  float(pd.DataFrame(df[a & b & c & d & e])['wts'].sum())
								if count!=0:
									counts.append(float(count))
								else:
									counts.append(0.000005)
			node.cpt_data['counts'] = counts
			net.normalise_cpt(X)

		curr_iter += 1

# Expectation-Maximisation
def Expectation_Maximisation(df, bn, mis_index):
	"""
	Input: 
		df - Data Table
		bn - Bayesian Network
		mis_index - array of missing indices corresponding to the Data table 'df'
	Output:
		bn - Bayesian Net with complete parameters learned from the given data by EM algorithm
	"""
	curr_iter = 1
	time_i = time.time()
	while True:
		print "ITERATION #" + str(curr_iter)
		step0 = time.time()
		# print "STEP E: "+ str(curr_iter)
		wts, new_df = Expectation(bn, df, mis_index)
		prev_cpts = []
		for X in bn.Pres_Graph.keys():
			prev_cpts.append(np.array(list(bn.Pres_Graph[X].cpt_data['p'])))
		step1 = time.time()
		# print "STEP M: "+ str(curr_iter)
		Maximisation(new_df, bn, wts)
		step2 = time.time()
		# print "E time: (%ss)" % (round((step1 - step0), 5))
		# print "M time: (%ss)" % (round((step2 - step1), 5))
		new_cpts = []
		for X in bn.Pres_Graph.keys():
			new_cpts.append(np.array(list(bn.Pres_Graph[X].cpt_data['p'])))
		diffs = []
		for i in range(len(prev_cpts)):
			max_diff = max(abs(np.subtract(prev_cpts[i],new_cpts[i])))
			diffs.append(max_diff)
		delta = max(diffs)
		time_f = time.time()
		print "Delta: " + str(delta)
		if ((time_f - time_i)>660):
			# print "OVER TIME. . . . "
			break
		if delta <= 0.00005:
			break
		curr_iter +=1
	print "Converged in (" + str(curr_iter) + ") iterations"

	return bn
		
# Parse learned parameters to 'solved_alarm.bif'
def parse_output(Alarm, bif_alarm):
	i = 0
	with open('solved_alarm.bif', 'w') as output, open(bif_alarm, 'r') as input:
		while True:
			line0 = input.readline()
			line = line0.strip()
			if line == '':
				break
			tokens = line.split()
			first_word = tokens[0]
			if first_word == 'table':
				X = Alarm.Pres_Graph.keys()[i]
				l = [X] + Alarm.Pres_Graph[X].Parents
				to_write = np.asarray(Alarm.Pres_Graph[X].cpt_data.sort_values(l, ascending = True)['p'])
				to_write = ["{:10.4f}".format(item) for item in to_write]
				to_write = str(to_write)[1:len(str(to_write))-1].replace("'", "")
				to_write = to_write.replace(",", "")
				to_write = to_write.replace("     ", " ")
				to_write = to_write.replace("    ", "")
				output.write('\ttable '+ to_write + " ;\n")
				i+=1
			else:
				output.write(line0)


if __name__ == '__main__':
	print "This file contains utility functions: Run main.py"




