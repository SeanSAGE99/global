### Library Revision: 1.0		
### Revision History
### No.		Author				Date		Comment
### 1.0		Tomasz Jankowski	2023-10-31	Original

### Dependencies

import java.lang.Throwable as JLException
import traceback


LOGGER = system.util.getLogger("AMS-GPPCA-scripting")

def runStopGPPCA(tagPath, deviceType, eventType, gppcaTagPath):

	'''
	Description:
	This function is used for creating GPPCA records in the Local and Remote (Oracle) Database. 
	It is tiggered by GP or PCA "Run " tag alarm. 

	Arguments: 	tagPath			- Tag Path of the Ground Power or Preconditioned Air Unit "Running" signal 
				deviceType		- "GP" or "PCA"
				eventType		- "S" for Start, "E" for End event
				gppcaTagPath	- GPPCA UDT instance tag path
	'''

	
	#gppcaTagPath = (default: GPPCA) for service points used in the bays with multi GP and PCA arrangemnts (some aircraft can use two or one GPU with one PCA at the same time)
	
	gppcaAlarmAreaPath = "[.]../" + gppcaTagPath + "/Parameters.Alarm_Area"
	gppcaBayNumberPath = "[.]../" + gppcaTagPath + "/Parameters.BayNumber"
	gppcaOldStatePath = "[.]../" + gppcaTagPath + "/Status/Old State"
	gppcaCorrelationIdPath = "[.]../" + gppcaTagPath + "/Status/Correlation ID"
	gppcaStartTimePath = "[.]../" + gppcaTagPath + "/Time/Start Time"
	gppcaEndTimePath = "[.]../" + gppcaTagPath + "/Time/End Time"
	gppcaStartEnergyPath = "[.]../" + gppcaTagPath + "/Energy/Start Energy"
	gppcaEndEnergyPath = "[.]../" + gppcaTagPath + "/Energy/End Energy"
	triggerFilter = 1 #initial value for appying start event trigger filter
	
	try:
	
		######### Check the status of Enable/Disable button (GPPCA interface enable state)		
		enableGPPCAqualifiedValues = system.tag.readBlocking("[~]Parameters/GPPCA/enableGPPCA")
		enableGPPCAvalue = enableGPPCAqualifiedValues[0]
		
		if enableGPPCAvalue.value and enableGPPCAvalue.quality.isGood():
		
			runQualifiedValues = system.tag.readBlocking(tagPath) #read value of the Running tag
			runValue = runQualifiedValues[0] # extract the qualified value from this list, there should only be 1 because we are reading a single tag value

			# Read old Start Time value to avoid bouncing of the trigger
			oldStartDateQualifiedValues = system.tag.readBlocking(gppcaStartTimePath)
			oldStartDateValue = oldStartDateQualifiedValues[0].value	
			dateTag = system.date.now() #date used in and "End Time" / "Start Time" tags
		
				
			if eventType == 'S': 
				expcetedRunValue = 1  #unit should be in a Running State 
				expcetedOldStateValue = 0 
				if system.date.millisBetween(oldStartDateValue, dateTag) > 60000: # checking the last start Time was less then a minute ago	
					triggerFilter = 1
				else:
					triggerFilter = 0
				LOGGER.error("Another Start Time detected less then 1 minute ago for a calling script tag: " + tagPath)		
			elif eventType == 'E':
				expcetedRunValue = 0 #unit should be in a Stop State 
				expcetedOldStateValue = 1
			else: LOGGER.error("Wrong device state for a calling script tag: " + tagPath)
				
	
			if runValue.value == expcetedRunValue and runValue.quality.isGood(): #check if the unit runnig state has expected value and tag quality is good
				# Reading previous value 
				oldStateQualifiedValues = system.tag.readBlocking(gppcaOldStatePath)
				oldStateValue = oldStateQualifiedValues[0] 
				# Reading date with different formats
				#dateTag = system.date.now() #date used in and "End Time" / "Start Time" tags
				date = system.date.format(dateTag, "yyyyMMddHHmmss") #date used in Correlation ID 
			
				if oldStateValue.value == expcetedOldStateValue:  #check if the unit has expected Running value in a previous state
				

					############################################ Get correlation ID
					
					# Read Terminal number
					alarmAreaQualifiedValues = system.tag.readBlocking(gppcaAlarmAreaPath)
					alarmAreaValues = alarmAreaQualifiedValues[0].value
					if ('T1' in alarmAreaValues) or ('International' in alarmAreaValues):
							terminal = 'T1'
					elif ('T2' in alarmAreaValues) or ('Domestic' in alarmAreaValues):
							terminal = 'T2'
					elif 'T3' in alarmAreaValues:
							terminal = 'T3'
					else:
							terminal = ''
							LOGGER.error("Alarm Area missing from the GPPCA UDT instance parameters for a calling script tag: " + tagPath)	
				
					# Reading Bay number
					bayNumberQualifiedValues = system.tag.readBlocking(gppcaBayNumberPath)					
					bayNumber = bayNumberQualifiedValues[0].value
					if bayNumber != None:
						# Pading Bay number with leading zeros to have always 5 characters for bay number (compatible with billing system redding from Oracle database)
						bayNumberCorID = bayNumber.zfill(5) #bay number used in correlation ID
					else: 
						bayNumberCorID = ''
						LOGGER.error("Bay number missing from the GPPCA UDT instance parameters for a calling script tag: " + tagPath)
					
					#Detect underscore suffix in bay number and keep only first half of string
					if "_" in bayNumber:
						bayNumberSplitDataSet = bayNumber.split("_")
						bayNumberDBentry = bayNumberSplitDataSet[0] #bay number used for database entry
					else:
						bayNumberDBentry = bayNumber
					
					# Reading type of the device - GP or PCA 
					if deviceType == 'GP':
						aircraftCode ='' #no aircraft code for GP transactions (only for PCA)
					elif deviceType == 'PCA':
						aircraftCodeQualifiedValues = system.tag.readBlocking("[.]Aircraft Code") #reading Aircraft Code 
						aircraftCode = aircraftCodeQualifiedValues[0]
						if aircraftCode.quality.isGood():
							aircraftCode = aircraftCode.value
						else:
							aircraftCode =''
							LOGGER.error("Aircraft Code missing from the PCA UDT instance parameters for a calling script tag: " + tagPath)
					else:	
						LOGGER.error("Wrong device type specified in the UDT instance for a calling script tag: " + tagPath)		
											
					# Writing correlation ID the unit is starting
					if eventType == 'S': 
						correlationID = date + terminal + bayNumberCorID + '_' + deviceType
						system.tag.writeBlocking(gppcaCorrelationIdPath,correlationID)
					elif eventType == 'E':
						# Reading correlation ID from the Memory Tag	
						corIDqualifiedValues = system.tag.readBlocking(gppcaCorrelationIdPath)
						corIDvalues = corIDqualifiedValues[0]
						if corIDvalues.value != "" and corIDvalues.quality.isGood():
							correlationID = corIDvalues.value 	
						else: 
							correlationID = ""
							LOGGER.error("Reading GPPCA correlation ID Tag error for a calling script tag: " + tagPath)
							
				
					############################################# Writing to Start Time, End Time and Energy Memory tags
					
					if eventType == 'S': 
						system.tag.writeBlocking([gppcaStartTimePath,gppcaEndTimePath],[dateTag,0]) #set Start Time and Reset the End Time when unit is running
						
						##### Read Power Meter Energy from the Input Meter
						meterReadingQualifiedValues = system.tag.readBlocking("[.]../Input Meter/Active Energy")
						if meterReadingQualifiedValues[0].quality.isGood():
							meterReadingValue = meterReadingQualifiedValues[0].value
						else: 
							meterReadingValue = 0
							LOGGER.error("Reading Input Meter Active Energy Fault for a calling script tag: " + tagPath)
						# Set Start and Reset End of Power Meter Energy readings when unit is running
						system.tag.writeBlocking([gppcaStartEnergyPath,gppcaEndEnergyPath],[meterReadingValue,0])
						meterEnergyConsumption = 0
						
					elif eventType == 'E':
						system.tag.writeBlocking(gppcaEndTimePath ,dateTag) #set End Time when unit is NOT Running
						
						#### Read Power Meter Energy from the Input Meter and Start Energy value from the Memory tag to calculate Energy Consumption
						meterReadingQualifiedValues = system.tag.readBlocking(["[.]../Input Meter/Active Energy",gppcaStartEnergyPath])
						if meterReadingQualifiedValues[0].quality.isGood() and meterReadingQualifiedValues[1].quality.isGood():
							meterReadingValue = meterReadingQualifiedValues[0].value
							meterReadingStartValues = meterReadingQualifiedValues[1].value
							meterEnergyConsumption =  meterReadingValue - meterReadingStartValues
						else: 
							meterReadingValue = 0
							meterEnergyConsumption = 0	
							LOGGER.error("Reading Input Meter Active Energy Fault for a calling script tag: " + tagPath)			
						# Set End of Power Meter Energy readings when unit is NOT Running
						system.tag.writeBlocking(gppcaEndEnergyPath,meterReadingValue)					
					
					############################################### Write to the database
					
					eventType = eventType + deviceType #S for starting event, E for ending event
					eventDate = system.date.format(system.date.now(), "dd-MMMM-yy")
					eventTime = system.date.format(system.date.now(), "dd:MMMM:yy hh:mm:ss a")
					
					try:
						#writing to the local database (remoteDBchecked':0,'remoteDBerror':0 added for future check both database consistnecy 
						params = {'eventType':eventType, 'bayNumber':bayNumberDBentry, 'terminal':terminal, 'meterReading':meterReadingValue,'energyConsumption':meterEnergyConsumption,'aircraftCode':aircraftCode, 'correlationID':correlationID,'eventDate':eventDate,'eventTime':eventTime,'remoteDBchecked':0,'remoteDBerror':0}
						system.db.runNamedQuery("AMS", "GPPCA/Add GPPCA in Local DB", params)
					except:
						LOGGER.error("Error in writing to the Local database for a calling script tag: " + tagPath)
					try:
						#writing to the remote database
						params = {'eventType':eventType, 'bayNumber':bayNumberDBentry, 'terminal':terminal, 'meterReading':meterReadingValue,'energyConsumption':meterEnergyConsumption,'aircraftCode':aircraftCode, 'correlationID':correlationID,'eventDate':eventDate,'eventTime':eventTime}
						system.db.runNamedQuery("AMS", "GPPCA/Add GPPCA in Remote DB", params)
					except:
						LOGGER.error("Error in writing to the Remote database for a calling script tag: " + tagPath)
					# When write sucessfull then change value of the old state tag to the current Running tag value
					system.tag.writeBlocking(gppcaOldStatePath,runValue.value)
				else:
					LOGGER.error("Old unit state value the same the current state for a calling script tag: " + tagPath)	
			else:
				LOGGER.error("Run status read tag error for a calling script tag: " + tagPath)				
		else:
			LOGGER.error("GPPCA interface not enabled")
	except Exception:
		LOGGER.error(traceback.format_exc())
		return -1
	except JLException:
		LOGGER.error(traceback.format_exc())
		return -1

			
						
									
															
def checkRemoteDatabase():

	'''
		Description:
		This function is used to compare local GPPCA database records with Remote (Oracle) database at the end of the day. 
		It is executed during curfew hours and when NO GPPCA transactions are triggered. 
		If some records are missing in Remote Database they will be added. Errors are registered in the AMS-GPPCA-scripting logger. 


		Arguments: N/A
		'''

	try:
	
		######### Check the status of Enable/Disable button (GPPCA interface enable state)		
		enableGPPCAqualifiedValues = system.tag.readBlocking("[default]Parameters/GPPCA/enableGPPCA")
		enableGPPCAvalue = enableGPPCAqualifiedValues[0]
			
		if enableGPPCAvalue.value and enableGPPCAvalue.quality.isGood():
	
			eventDate = system.date.format(system.date.now(), "dd-MMMM-yy")
			params = {'eventDate': eventDate}
			
			data = system.db.runNamedQuery("AMS", "GPPCA/Local DB Check", params) #check all records for the day in the local DB
			 
			LOGGER.trace("lets start")
			
			for row in data:
				eventType = row["DATA_EVENT_TYPE"]
				correlationID = row["CORRELATION_ID"]
				params1 = {'eventType':eventType, 'correlationID':correlationID}
				
				try:
					recordCheck = system.db.runNamedQuery("AMS", "GPPCA/Remote DB Record Check", params1) #check if that record exsit in remote DB 
					recordExistinRemoteDB = recordCheck[0][0]
					if recordExistinRemoteDB:
						params2 = {'eventType':eventType, 'correlationID':correlationID, 'remoteDBchecked':1,'remoteDBerror':0}
						addingToLocalDB = system.db.runNamedQuery("AMS", "GPPCA/Amend Local DB", params2)
						LOGGER.trace("Amend local Database with setting remoteDBchecked to 1 and remoteDBerror to 0")
					else:
						LOGGER.trace("Missing record to be added")
						bayNumber = row["BAY_NUMBER"]
						terminal = row["TERMINAL"]
						meterReadingValue = row["METER_READING"]
						meterEnergyConsumption = row["ENERGY_CONSUMPTION"]
						aircraftCode = row["AIRCRAFT_CODE"] 
						eventDate = row["EVENT_DATE"] 
						eventTime = row["EVENT_TIME"] 
						try:
							#add missing record to the Remote Database, 
							params3 = {'eventType':eventType, 'bayNumber':bayNumber, 'terminal':terminal, 'meterReading':meterReadingValue,'energyConsumption':meterEnergyConsumption,'aircraftCode':aircraftCode, 'correlationID':correlationID,'eventDate':eventDate,'eventTime':eventTime}
							addingToRemoteDB = system.db.runNamedQuery("AMS", "GPPCA/Add GPPCA in Remote DB", params3)
							#update Local Databse to indicate that corresponding record was checked withour errors
							params2 = {'eventType':eventType, 'correlationID':correlationID, 'remoteDBchecked':1,'remoteDBerror':0}
							addingToLocalDB = system.db.runNamedQuery("AMS", "GPPCA/Amend Local DB", params2)
							LOGGER.trace("Sucessfull write to Remote Database")
						except:
							LOGGER.error("Error Writing to remote Database")
							#write Remote DB communication error to the local database for corresponding record
							params4 = {'eventType':eventType, 'correlationID':correlationID, 'remoteDBchecked':0,'remoteDBerror':1}
							system.db.runNamedQuery("AMS", "GPPCA/Amend Local DB", params4)
						#if not sucessfull then writ error to Local Database
				except:
					LOGGER.error("Error Reading from Remote Database")	
		else:
			LOGGER.error("GPPCA interface not enabled")
		
	except Exception:
		LOGGER.error(traceback.format_exc())
		return -1
	except JLException:
		LOGGER.error(traceback.format_exc())
		return -1		