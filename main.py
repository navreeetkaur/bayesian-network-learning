import sys
import time
import utils


# Setup network
step0 = time.time()
print "Initialising . . . . " 
bn, df, mis_index = utils.setup_network(sys.argv[1], sys.argv[2])
step1 = time.time()
print "Initialisation time: (%ss)" % (round((step1 - step0), 5))
print
# Learn parameters
print "Expectation-Maximisation . . . . "
Alarm = utils.Expectation_Maximisation(df, bn, mis_index)
step2 = time.time()
print
print "EM time: (%ss)" % (round((step2 - step1), 5))
print
print "Parsing output file . . . . "
utils.parse_output(Alarm, sys.argv[1])
step3 = time.time()
print "Output file parsing: (%ss)" % (round((step3 - step2), 5))
print
print "TOTAL Time taken: (%ss)" % (round((step3 - step1), 5))