### Library Revision: 1.0		Increment with any change to the functions within

def getTemplateRootContainer(component):
	'''
	Description:
		Return the Template root object so that Template parameters may be accessed.
		This is the equivalent to system.gui.getParentWindow(event).rootContainer for a Window.
		Note: this can still be run within a template, however you will get the Window's rootContainer and not the Template root object!
	
	Arguments:
		component		- usually this would be passed    event.source    when it is called from a component event handler script.
	
	Usage:
		Call this on components within a Template.
	
	Revision:
		No.		Date		Author			Comment
		1.0		2018-11		Nick Minchin	Original
	'''
	
	# This is the type of a template object. This is the object type that we're looking for.
	templateObjTypeStr = str("<type 'com.inductiveautomation.factorypmi.application.components.template.VisionTemplate'>")
	objTypeStr = ''
	loopCount = 0
	obj = None
	
	# Loop through the parent components of the initial component until we find the first template type. Limited to a depth of 10 levels   
	while objTypeStr != templateObjTypeStr and loopCount < 10:
		if obj == None:
			obj = component
		else:
			obj = obj.parent
			
		objTypeStr = str(type(obj))
		loopCount += 1
	
	foundTemplate = 0
	if objTypeStr == templateObjTypeStr:
		foundTemplate = 1
		return obj
	else:
		return None