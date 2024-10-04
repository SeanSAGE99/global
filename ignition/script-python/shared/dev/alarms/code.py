def getAnyActiveExpression(pathToAlarmsFolder):
	"""
	Produces the expression for an _AnyActive expression tag if required.
	"""
	alarm_tag_names = shared.tag.browseTags(pathToAlarmsFolder)
	alarm_tag_names = [tag['name'] for tag in alarm_tag_names if tag['name'] != '_AnyActive']
	any_active_expression = '{[.]' + '} || \r\n{[.]'.join(alarm_tag_names) + '}'
	
	return any_active_expression