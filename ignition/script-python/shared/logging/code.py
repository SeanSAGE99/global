def writeAuditLog(actor, actorHostName, actionType, actionTarget, actionValue, context):
	'''
	string actor:			person or process performing the action 
	string actorHostName:	hostname of the actor
	string actionType:		the type of action performed (tag write etc.)
	string actionTarget:	the target of the action, e.g. the tag path
	string actionValue:		the value written to the action type e.g. 1022
	int context:			what system the action was performed on: 1 - Gateway, 2 - Designer, 4 - Client
	
	'''
	timestamp = system.date.format(system.date.now(), 'yyyy-MM-dd HH:mm:ss')
	status = 0
	origSystem = 'project=' + system.util.getProjectName()
	
	sql = 'INSERT INTO AUDIT_EVENTS (EVENT_TIMESTAMP, ACTOR, ACTOR_HOST, ACTION, ACTION_TARGET, ACTION_VALUE, STATUS_CODE, ORIGINATING_SYSTEM, ORIGINATING_CONTEXT) VALUES '
	sql += "(?,?,?,?,?,?,?,?,?)"
	system.db.runPrepUpdate(sql,
						   [timestamp, actor, actorHostName, actionType, actionTarget, actionValue, status, origSystem, context],
						   'SQLServer')