'''
Revision History
1.0	2021-05-11	Original	Zander Minchin
'''

import os

def dirToData(path,user):

	general = "general"
	if user is None:
		user = "Guest"
	
	data = []
	for root, subdirs, files in os.walk(path):
		for file in files:
			if (user in root) or (general in root):
				fullPath = os.path.join(root,file).replace('\\','/')				
				d = {"Config" : file, "Path" : fullPath}
				if user in root:
					d['Config'] = {"value" : file, "style" : {}}
					d['Config']['style']['color'] = 'var(--info)'
				data.append(d)
	return data


def dirToDict(path):
	'''
	Description:
		This function walks recursivley through a directory and its subdirecrories and stores
		the file and folder structure into a dictionary object
		
	Pre-Requisites:
		import os
		
	Arguments:
		path : the path to the parent directory
		
	Return:
		python dictionary object containing the files and subdirectories
		
	Usage:
		Call this function and pass in the result to the setTreeProps function 
	
	Revision:
		No.		Date		Author			Comment
		1.0		2021-05-11	Zander Minchin	Original
	'''
	
	directoryDict = {'label': os.path.basename(path)}
	directoryDict['expanded'] = True
	directoryDict['data'] = path
	if os.path.isdir(path):
		directoryDict['items'] = [dirToDict(os.path.join(path,x)) for x in os.listdir(path)]
	return directoryDict
	
	
def setPowerChartProps(jsonPropsFilePath, powerchartObj):
	'''
	Description:
		This function exctracts properties from a JSON file and loads only the required properties 
		into a PowerChart object
		
	Pre-Requisites:
		
	Arguments:
		jsonPropsFilePath : the path to the JSON file to be loaded
		powerchartObj : a PowerChart component, eg self.parent.getChild("PowerChart")
		
	Return:
		None : it sets the properties of the powerchartObj
		
	Usage:
		Call this function to load a trend config from a json file into a Power Chart 
	
	Revision:
		No.		Date		Author			Comment
		1.0		2021-05-11	Zander Minchin	Original
	'''
	selectedFile = system.file.readFileAsString(jsonPropsFilePath)
	jsonFile = system.util.jsonDecode(selectedFile)	 

	chartProps = ['config', 'interaction', 'axes', 'pens', 'plots'
			, 'dataColumns', 'title', 'timeAxis', 'legend', 'style']	 

	# explicitly assign only properties that are needed for chart
	newProps = {}
	for prop in chartProps:
		newProps[prop] = jsonFile[prop]
			
	powerchartObj.props = newProps
		

def sanitiseTree(element):
	'''
Description:
	######## TO DO #############
	
Pre-Requisites:
	import os
	
Arguments:
	path : the path to the parent directory
	
Return:
	sanatised element
	
Usage:
	call this function and pass in the result to the setTreeProps function 

Revision:
	No.		Date		Author			Comment
	1.0		2021-05-11	Nick Minchin	Original
'''
	if hasattr(element, '__iter__'):
		if hasattr(element, 'keys'):
			return dict(zip(element.keys(), (sanitiseTreeree(element[k] for k in element.keys()))))
		else:
			return list(sanitiseTree(x) for x in element)
	return element