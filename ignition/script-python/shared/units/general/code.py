### Library Revision: 1.1		Increment with any change to the functions within

def initUnitDSs(unitPath, tempRepeater):
	'''
	Description:
	Initialises the datasets required for a unit popup (Popups/ppuUnit) to display the unit parameters.
	
	Requirements:
	This function writes into custom dataset parameters defined in the Unit popup's root window container. These must exist:
	- rootContainer.UnitParamsDS
	
	IMPORTANT NOTE:
	After executing this function, make sure to perform a refresh on the UP template repeaters's templateParams dataset! Otherwise, if this returns an empty dataset, the component will
	display the UPs from the previously opened device. 
	'''
	
	#Read the configured unit parameters from the unit tags and write them into a dataset to use with the unit params template repeater
	ds = getUnitParamsDS(unitPath)
	
	print tempRepeater.templateParams
	print ds
	tempRepeater.templateParams = ds
	print tempRepeater.templateParams


####
#### Helper functions
####

def getUnitParamsDS(unitPath):
	'''
	Description:
	Returns a dataset with the Unit Parameter details of a Unit so that these can be displayed in a template repeater using the template: [shared]Units/Unit Param
	
	Requirements:
	Expects the unit parameter tags to use the standard unit definition. This means that the unit path has at least this unit parameter tag structure:
		Unit Parameters/<Tag Name> [OPC], where <Tag Name> is the descriptive name of the unit parameter that reads its value from the PLC. 
	'''
	#retrieve a list of all of the step tags for the sequence. This returns a list of BrowseTag objects.
	#print 'Unit path: ', unitPath 
	unitParamTags = system.tag.browseTagsSimple(unitPath + '/Unit Parameters', 'ASC')
	
	#we want to display the eng parameters in the correct order, based on the PLC tag name (EP01-xx), so we read the OPCItemPath of the tags
	unitParamOPCItemPathTags = [tag.path + '.OPCItemPath' for tag in unitParamTags]
	unitParamOPCItemPaths = system.tag.readAll(unitParamOPCItemPathTags)
	unitParamOPCItemPaths = [tag.value for tag in unitParamOPCItemPaths] #store just the value of the browseTag object. This is the opc item path string.
	
	#produce a list of the tag names. we don't need the path as we have the sequencePath already and assume that these tags are in: <sequencePath>/Engineering Parameters/<tag.name>
	unitParamTags = [tag.name for tag in unitParamTags]
	
	#combine the OPCItemPaths with side-by-side with the tag names into a combined list.
	unitParamTags = zip(unitParamTags, unitParamOPCItemPaths)
	
	#create the dataset column names. We exclude the BGColour first as we need to sort the dataset by the OPCItemPath first before setting these.
	dshdr = ['TagName', 'UnitTagPath', 'OPCItemPath']
	dsdata = []
	
	for unitParamTag in unitParamTags:
		#append the current eng param details to the dataset
		#print '   Adding tag: ',unitParamTag[0] 
		dsdata.append([unitParamTag[0], unitPath, unitParamTag[1]])
		
	ds = system.dataset.toDataSet(dshdr,dsdata)
	ds = system.dataset.sort(ds, 'OPCItemPath', 1)
	ds = system.dataset.toPyDataSet(ds)
	
	dsList = []
	BGColour = 0
	for row in ds:
		dsList.append([row[0], row[1], row[2], BGColour])
		BGColour = not BGColour
	
	if len(dsList) == 0:
		dsList 
	
	dshdr = ['TagName', 'UnitTagPath', 'OPCItemPath', 'BGColour']
	ds = system.dataset.toDataSet(dshdr, dsList)
	
	return ds