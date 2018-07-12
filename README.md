# Bayesian Network Parameter Learning
### Course Project - COL884(Spring'18):Uncertainity in AI
#### Creator: Navreet Kaur[2015TT10917]

#### Objective: 
Bayesian Parameter Learning of Alarm Bayesian Net given data with at most one missing value in each row.
#### Algorithm Used: 
Expectation-Maximisation
#### Goal: 
The goal of this assignment is to get experience with learning of Bayesian Networks and understanding their value in the real world. 
#### Scenario: 
Medical diagnosis. Some medical researchers have created a Bayesian network that models the inter-relationship between (some) diseases and observed symptoms. Our job as computer scientists is to learn parameters for the network based on health records. Unfortunately, as it happens in the real world, certain records have missing values. We need to do our best to compute the parameters for the network, so that it can be used for diagnosis later on.
#### Problem Statement: 
We are given the Bayesian Network created by the researchers(as shown in BayesNet.png).Notice that eight diagnoses are modeled here: hypovolemia, left ventricular failure, Anaphylaxis, insufficient analgesia, pulmonary embolus, intubation, kinked tube, and disconnection. The observable nodes are CVP, PCWP, History, TPR, Blood Pressure, CO, HR BP, HR EKG, HR SAT, SaO2, PAP, MV, Min Vol, Exp CO2, FiO2 and Pres. Such networks can be represented in many formats. We will use the .bif format. BIF stands for Bayesian Interchange Format. The details about the format are [here](http://sites.poli.usp.br/p/fabio.cozman/). We are also providing a .bif parser so that you can start directly from a parsed Bayesian network represented as a graph.

The goal of the assignment is to learn the Bayes net from a healthcare dataset.
#### Input format:
We will work with alarm.bif network. Please have a look at this file to get a basic understanding of how this information relates to the Bayes net image above. A sample Bayes net is as follows
variable “X” {

type discrete[2] { “True” “False” };

}

variable “Y” {

type discrete[2] { “True” “False” };

}

variable “Z” {

type discrete[2] { “True” “False” };

}
probability(“X”) { table 0.2 0.8 ; }

probability(“Y”) { table 0.4 0.6 ; }

probability(“Z” “X” “Y”) { table 0.2 0.4 0.3 0.5 0.8 0.6 0.7 0.5; }

This says that X, Y, and Z all have two values each. X and Y has no parents and prior P(X=True)=0.2, P(X=False)=0.8, and so on. Z has both X and Y as parents. Its probability table says P(Z=True|X=True, Y=True) = 0.2, P(Z=True|X=True, Y=False) = 0.4 and so on.

Our input network will have the Bayes net structure including variables and parents, but will not have probability values. We will use -1 to represent that the probability value is unknown.
probability(“X”) { table -1 -1 ; } will represent that prior probability of X is unknown and needs to be computed via learning.

To learn these values we will provide a data file. Each line will be a patient record. All features will be listed in exactly the same order as in the .bif network and will be comma-separated. If a feature value is unknown we will use the special symbol “?” for it. There will be no more than 1 unknown value per row. Example:

“True”, “False”, “True” “?”, “False”, “False”

Here the first row says that X=True, Y=False and Z=True. The second row says that X is not known, Y and Z are both False.
Overall your input will be alarm.bif with most probability values -1 and this datafile. The datafile will have about 10,000 patient records.
#### Output format:
Output will be the result of learning each probability value in the conditional probability tables. In other words, all -1s are replaced with a probability value upto four decimal places. Thus, the output is a complete alarm.bif network.
#### Files:
1) records.dat:
	A Dataset file where a single line is a single patient record and each variable in the record is separated by spaces. The unknown record is marked by “?”. Each line contains at max 1 missing record. The file contains more than 11000 records.
2) format_check.cpp: 
	A format checker to check your output file adheres to alarm.bif format. The format checker assumes that alarm.bif, solved_alarm.bif and gold_alarm.bif are present in current directory and outputs its results. (A next version will also compute the total learning error).
3) Alarm.bif:
	BIF format file, whose parameters need to be learned
4) Gold_Alarm.bif:
	BIF file having the true parameters
5) bayesnet.py:
	classes: 	
		Graph_Node
		Network
	methods:
		read_network: Parsing the .bif format file and build a bayesian net
		markov_blanket: Get variables in the markov blanket of variable 'val_name'	
		get_data: Read data from records.dat and store as a pandas dataframe 
		normalise_counts: normalise a list of counts from a given CPT	
6) utils.py:
	methods:
		setup_network
		get_missing_index: List of the indices of nodes which have missing values in each data point; equal to -1 if 		     no value is missing
		init_params: Initialise parameters
		normalise_array: Normalise a numpy array
		get_assignment_for: return the rows of the factor table with assignments as specified in evidence E
		markov_blanket_sampling: Inference by Markov Blanket Sampling
		Expectation 
		Maximisation
		Expectation_Maximisation
		parse_output
7) main.py: main file that calls methods from bayesnet and utils to build a bayes net, read data and learn its parameters
#### Compilation:
Run the file run.sh - it takes 2 input files, alarm.bif and records.dat and output a file named
solved_alarm.bif file:
`./run.sh alarm.bif <sample_data>.dat`

#### Assumptions:
• All variables are missing completely(or unconditionally) at random(MCAR) and none of them are either missing at random(MAR) or missing systematically or hidden i.e. initially, probability of each missing value is the same and the sample mean of variable v is unbiased estimator of true value of v
#### Parameter Initialisation:
• Initialisation of parameters by available case analysis(ignoring rows with missing values if the missing value is that of the parent). Since data is MCAR, estimators based on the subsample of the data are unbiased estimators for the ones with complete data
#### Design Choices:
1. Data Records:
(a) String values for each class of random variables were mapped to integers
(b) Data File was stored as a Pandas DataFrame so as to perform grouping and aggregation of certain data occurrences to get theirs counts 
2. Network
(a) Ordered dictionary to represent nodes in the graph (keys = name of random variable, value = node object)
(b) Ordered dictionary to store Markov Blanket(MB) of all nodes (keys = name of random variable(X), value = list of Strings of names of nodes in MB of X) - This is stored so as to avoid recomputation of Markov Blanket at each step while doing Markov Blanket Sampling Inference
3. Graph_Node
(a) List of Strings to store names of Parents
(b) List of integers to store indices of Children in ordered dictionary of nodes in Bayes Net
(c) Pandas DataFrames to store CPT
4. CPTs
(a) All CPTs are represented by Pandas DataFrames(columns are names of variables and column ‘p’ for probability value) so as to easily access the entries by specifying a dictionary of ‘Evidence’ with keys as variable names and values as the integers
#### Optimisation/Techniques:
1. Storage of only counts and not probabilities in all the CPTs and normalising them before performing Expectation step
2. **Smoothing**: Since all possible instances might not be observed due to small size of dataset as compared to number of network nodes, counts of all possible instances in the CPTs were set to one to initialise with. Similarly, in the Maximisation step, with any observed count was equal to zero, it was set to 0.00005 (since required precision of probabilities is upto 4 decimal places and counts in maximisation might be less than one due to weights of data points being considered, which itself lie between 0 and 1) 
3. **Inference**: Since the probability of variable X is independent of all other variables given its markov blanket and only one data point is missing per row(i.e. all points are given hence MB is given), therefore, P(X | data) = P(X | mb(X)), where mb(X) is the markov blanket of x. Therefore, markov blanket sampling was used to calculate P(X | MB(X))
4. Using **log probabilities** as addition operation is faster than multiplication and also, it helps to avoid numerical underflow.
5. **Convergence Criteria**: Maximum change in the CPTs in previous and current iteration is less than equal to 0.00005
