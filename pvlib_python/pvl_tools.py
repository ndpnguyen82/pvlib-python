import pdb
import numpy as np 
import ast
import re

class repack():   #repack a dict as a struct
	def __init__(self,dct):
		self.__dict__.update(dct)

class Parse():		#parse complex logic
	

 	def __init__(self, dct, Expect):
 		self.__dict__.update(self.parse(dct,Expect))

	def parse(self,kwargs,Expect):
		#pdb.set_trace()
		#Check all inputs are defined
		try:
			for arg in kwargs:
				Expect[arg]
		except:
			raise Exception('WARNING: Unknown variable " '+arg+' " ')

		#Check that all inputs exist
		try: 
			for arg in Expect:
				if 'df' in Expect[arg]:
					df=kwargs[arg]  #locate main dataframe 
				if not(('matelement' in Expect[arg]) or ('optional' in Expect[arg]) 
						or ('default' in Expect[arg])):
					kwargs[arg]
		except:
			raise Exception('WARNING: " '+arg+' " was not input')	

		
		#Check dataframe entries
		try:
			for arg in Expect:
				if 'matelement' in Expect[arg]:
					df[arg]

		except:
			raise Exception('WARNING: " '+arg+' " in main dataframe does not exist')			
		# Assert numeric for all numeric fields
		
		try:
			for arg in kwargs:
				#add any exceptions to numeric checks (eg. string input fields)
				if not('num' in Expect[arg]):
					continue
				# Check if the value is an np.array
				if not isinstance(kwargs[arg],np.ndarray):
		 			kwargs[arg]=np.array(kwargs[arg])
		 			print('WARNING: Numeric variable '+ arg +' not input as a numpy array. Recasting as array')
				kwargs[arg].astype(float)
		except:
			raise Exception('Error: Non-numeric value in numeric input field: '+arg)

		#Check any string inputs. 
		#pdb.set_trace()
		print 'DEVWARNING: Fix string index dependancy'
		for arg in kwargs:
			if 'str' in Expect[arg]:
				if (not('open' in Expect[arg]) or not( 'o' in Expect[arg])) and not(kwargs[arg] in Expect[arg][1]):
					raise Exception('Error: String in input field '+ arg+' is not valid')


		#Check logical functions
		#pdb.set_trace()
		reg=re.compile('[a-z][== <= >= < >][== <= >= < >]?-?[0-9]+')
		reglogical=re.compile('.[== <= >= < >].')
		regdefault=re.compile('default=')
		regsyst=re.compile('.__.')
		for arg in Expect:
			for string in Expect[arg]:
				
				if isinstance(string,basestring): ##Python 2.x dependancy
					#Remove any potential of running system commands through eval
					if np.shape(re.findall(regsyst,string))[0]>0:		
						raise Exception("DANGER: System Command entered as constraint ' "+ string+ "' ")	
					#Set default value for a variable if defined
					elif np.shape(re.findall(regdefault,string))[0]>0:
						
						try: 
							kwargs[arg]
					 	except:
					 		try: 
								kwargs[arg]=np.array(float(string[8:])) #numeric defualt
							except:
								kwargs[arg]=(string[8:]) #string default
					#Excecute proper logical operations if syntax matches regex
					elif np.shape(re.findall(reg,string))[0]>0:
						lambdastring='lambda x:'+re.findall(reg,string)[0]
						#check df elements
						if ('matelement' in Expect[arg]):
							if not(eval(lambdastring)(df[arg]).any()):
								raise Exception('Error: Numeric input "'+arg+' " fails on logical test " '+ re.findall(reg,string)[0]+'"')	
						#check all other contraints
						elif not(eval(lambdastring)(kwargs[arg]).all()):
							raise Exception('Error: Numeric input "'+arg+' " fails on logical test " '+ re.findall(reg,string)[0]+'"')
					#Check if any string logicals are bypassed due to poor formatting
							
					elif np.shape(re.findall(reglogical,string))[0]>0:		
						raise Exception("WARNING: Logical constraint ' "+string+" ' is unused. Check syntax")
					
			 	

		return kwargs


	# if kwargs['Pressure']<0:
	# 	raise Exception('Pressure Cannot be negative')
	
	# for arg in kwargs:
	# 	if not isinstance(kwargs[arg],np.ndarray):
	# 		kwargs[arg]=np.array(kwargs[arg])

	# AMrelative=kwargs['AMrelative']
	# pressure=kwargs['Pressure']