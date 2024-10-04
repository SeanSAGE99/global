#periodVal E.g. 4
#periodType	= 'ms', 's', 'min', 'h', 'd', 'w', 'month', 'yr'
def setPeriod(chartObj, periodVal, periodType, retNewDate=0):
	endDate = chartObj.endDate
	
	#Convert the periodType into the end of the function name e.g. add<Days> 
	fncName = {'ms':'Millis', 's':'Seconds', 'min':'Minutes', 'h':'Hours', 'd':'Days', 'w':'Weeks', 'month':'Months', 'yr':'Years'}.get(periodType, '')
	
	addFunction = getattr(system.date, 'add' + fncName)
	#Need to negate the periodVal since the start time needs to be endDate - periodVal
	startDate = addFunction(endDate, -1*periodVal)
	
	if retNewDate:
		return startDate
	else:
		chartObj.startDate = startDate
		chartObj.outerRangeStart = system.date.addMinutes(startDate, -5)
		chartObj.outerRangeEnd = system.date.addMinutes(endDate, 5)


#Set view to Now, maintaining the current view window.
def moveToNow(chartObj):
	endDate = chartObj.endDate
	startDate = chartObj.startDate
	chartRange = system.date.secondsBetween(endDate, startDate)
	
	#Add 5s to now for a small blank space at the end of the chart view.
	endDate = system.date.addSeconds(system.date.now(),int(5*60))
	startDate = system.date.addSeconds(endDate, chartRange)
	
	#Cannot set the endDate more than 365 days past the startDate
	#therefore, if the current range is more than a year ago, we need
	#to set this multiple times to get to Now()
	exitLoop = 0
	while chartObj.endDate != endDate and exitLoop < 100:
		chartObj.endDate = endDate
		chartObj.startDate = startDate
		exitLoop = exitLoop + 1