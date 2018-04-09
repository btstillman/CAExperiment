import CA
import pandas as pd
from numpy import arange


class CAExperiment:
    #label -- what we are calling this particular experiment (corresponds to what we have in the .pdf file)
    #rule -- the CA rule to use
    #rule_radius -- the radius for the CA file
    #initial_ensemble -- the list of initial configurations to use
    #config_length -- the length of each configuration in the ensemble
    #num_generations -- the number of generations to run the CA
    #func_list -- the functions to apply to the spacetime diagrams
    #var_list -- a list of the variable name for each function (crucial)
    #measurement_list -- a data frame holding the relevant measurements from each spacetime diagram
    #report_file -- the .csv file to which we write the report

    def __init__(self,label=None,rule=None,rule_radius=0,init_ensemble = [],config_length=0,num_generations = 0,
                 func_list=[], var_list=[],measurement_list=[],report_file=None):
        self.label = label
        self.rule = rule
        self.rule_radius=rule_radius
        self.init_ensemble = init_ensemble
        self.config_length = config_length
        self.num_generations = num_generations
        self.func_list=func_list
        self.var_list = var_list
        self.measurement_list=var_list
        self.report_file = report_file

    def read_initial_ensemble(self, init_ensemble_file):
        '''
        read_init_ensemble, takes an input file (.txt) of numbers and converts those to configurations

        ARGS:
        init_ensemble, a file object containing configurations being used as the initial configurations in the experiment
        first line should be configuration length

        RETURNS:

        '''
        #reset the ensemble since it is going to be whatever is in the file
        self.init_ensemble = []
        temp_ensemble = []
        f = init_ensemble_file.readlines()
        #the first line should be the configuration length
        config_length_to_use = f[0]
        #set the configuration length of the object
        self.config_length = config_length_to_use
        for i in range(1,len(f)):
            #first get the config number
            config_num = int(f[i])
            config_to_add = CA.make_config(config_num, config_length_to_use)
            temp_ensemble.append(config_to_add)
        self.set_init_ensemble(temp_ensemble)

    def write_initial_ensemble(self, init_ensemble_file):
        '''
        write_init_ensemble, takes a list of configurations and writes them to a file

        ARGS:
        init_ensemble_file, a file to which the configuration numbers should be written
        RETURNS:

        updated: Bstillman
        '''
        f_open = open(init_ensemle_file, 'w')
        f_open.write( " Initial Ensemble \n")
        for  ensemble in init_ensemble :
            f_open.write( str(ensemble) + "\n" )
        f_open.close()

    def read_func_list(self, pickled_file):
        '''
        read_func_list, takes a list of

        ARGS:

        RETURNS:
        func_list, the list of functions being used
        '''
        f_file = open( pickled_file, 'r') # opens file
        self.func_list = [] # clears variable
        for fline in f_file:
            self.func_list.append(fline) # stores each function in the list
        f_file.close()
        return self.func_list
        
        

    def write_func_list(self,pickled_file): # Russian Mistake selfself?
    '''
    write_func_list, reads a function list file and appends its contents to the existing function list.
    
    ARGS: pickled_file,  the function file to be read
    
    RETURNS: 
    
    
    '''
        pf_file = open( pickled_file, 'r') # opens file
        for fline in pf_file:
            self.func_list.append(fline) # appends the new function to the existing func list.
        pf_file.close()
    #end (no returns?)
        
        
     
     ##

    def add_func(self, func_to_add, var_to_add):
        '''
        add_func, add a function to the current func_list

        ARGS: func, a function to add

        RETURNS:

        '''
        append(self.func_list,func_to_add)
        append(self.var_list, var_to_add)

    def add_funcs(self,funcs_to_add,vars_to_add):
        '''
        add_funcs, add a list of functions to the current func_list

        ARGS: func, a function to add

        RETURNS:

        '''
        self.func_list =  self.func_list + funcs_to_add
        self.vars_list = self.var_list + vars_to_add

    def run_experiment(self,rule=self.rule,init_ensemble=self.init_ensemble):
        '''
        run_experiment, creates a list of spacetime diagrams for a set of rules and initial configurations

        ARGS: func, a function to add

        RETURNS: data_log, a list of space-time diagrams for these initial configurations

        '''
        rule_table = CA.make_rule_table(rule,self.radius)
        data_log = []
        for config in init_ensemble:
            data = CA.evolve(rule_table,self.rule_radius,config,self.config_length,self.num_generations)
            data_log.append(data)
        return data_log

    def make_measurements(self, experiment_log, func_list = self.func_list, var_list = this.var_list):
        #we will always start with the rule number, the radius, the configuration number, and the configuration length
        set_vars = ['rule','radius','config','config_length']
        #add the experimenter's defined variables onto the list
        useful_vars = set_vars + var_list

        measurement_log = pd.DataFrame(columns=useful_vars,index=arange(0,len(experiment_log)))
        #loop over each spacetime diagram in the experiment log
        #create counter for data frame location (row number)
        i = 0
        for diagram in experiment_log:
            #create a blank row
            row_to_add = []
            #for each function, evaluate it on the diagram
            for func in func_list:
                data_to_add = func(diagram)
                #check to see how to add it on
                if data_to_add is list:
                    row_to_add = row_to_add + data_to_add
                else:
                    row_to_add.append(data_to_add)
            #add the row to the data set
            test.loc[i] = row_to_add
            #increment the variable to keep the row index correct
            i = i + 1
        return measurement_log



    #TODO: finish write_report
    #write the data frame resulting an experiment (applying functions to rules evaluated on ensembles) to a .csv file
    #if no .csv file provided, create one with the name of the CAExperimenter object

    def write_report(self, measurement_log, file_to_write=None):
        #if no file is supplied, use the label to create the file name
        if file_to_write == None:
            name_to_write = self.__name__
            file_to_write = fopen(str(self.__name__ + ))
            #TODO: finish this
        else:
            file_to_write = self.report_file
        out = csv.writer(open(self.report_file,"a+"), delimiter=',')
        for measurement in measurement_log:
            out.writerow(measurement)
            
        # will need to add more nuance to this approach so we will have better documented experiments

## CA.py code

