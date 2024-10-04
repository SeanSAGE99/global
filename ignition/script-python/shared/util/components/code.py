# traverse all components within an object and print them and their component index reference to the screen
def printAllObjectComponents(object, indexPrefix = '', indent = ''):
	components = object.getComponents()
	for index, component in enumerate(components):
		print "%s %s%s %s" % (indent, indexPrefix, index, component)
		
		printAllObjectComponents(component, indexPrefix + str(index) + '.', indent + '\t')


# traverse all components within an object and print them and their component index reference to the screen
def getAllObjectComponents(object, componentsList=[]):
	components = object.getComponents()
	for index, component in enumerate(components):
		componentsList.append(component)
		
		getAllObjectComponents(component, componentsList)
	return componentsList