def getInterlocks(deviceName, deviceParentPath):
	'''
	Description:
	Returns a dataset with the interlocks configured for a device.
	This dataset should be displayed in a template repeater using the template: [shared]Devices/_Parts/Interlocks
	
	Requirements:
	Expects the interlock tags to be created within the device under:
		Interlocks/Description 
	'''
	
	deviceTagPath = deviceParentPath + '/' + deviceName
	#retrieve a list of all of the interlock tags for the device. This returns a list of BrowseTag objects. 
	interlockTags = system.tag.browseTagsSimple(deviceTagPath + '/Interlocks', 'ASC')
	#produce a list of the tag names only
	interlockDescs = [tag.name for tag in interlockTags]
	
	#the dataset column names
	dsHeader = ['DeviceTagPath', 'InterlockDesc', 'BGColour']
	dsData = []
	
	#this variable is used to show alternating row colours
	BGColour = 0
	for interlockDesc in interlockDescs:
		dsData.append([deviceTagPath, interlockDesc, BGColour])
		BGColour = not BGColour
	
	return system.dataset.toDataSet(dsHeader,dsData)
