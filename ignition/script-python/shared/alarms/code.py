# 
# Revision History
# 1.0	xx-xx-xxxx	Nick Minchin	Original
# 1.1 	xx-xx-xxxx Tomasz Jankowski Added condition to not shot diagnostic alarms
import java.lang.Throwable as JLException
from java.lang.System import nanoTime
import traceback
import copy
import re
from operator import itemgetter

LIBRARY = 'shared.be.alarms'
LOGGER = system.util.getLogger('SAGE-Scripting-{}'.format(LIBRARY))



def getAlarmTags(pathFilter='*'):
	tags = system.tag.getConfiguration(pathFilter, True)
	alarms = getAlarmsFromFolder(pathFilter, tags)
	
	return alarms

def getAlarmsFromFolder(pathFilter, tags, tagPath=None):
	"""
	Description:
		Returns a list of alarms and their basic info as a dict 
	"""
	if tagPath is None: tagPath = ''
	
	pathFilter = pathFilter[:-1] if pathFilter[-1] == '/' else pathFilter
	parentFolder = '/'.join(pathFilter.split('/')[:-1])
	
	alarms = []
	for tag in tags:
		thisTagPath = tagPath
		if tagPath != '':
			thisTagPath = tagPath + '/' + tag['name']
		else:
			thisTagPath = tag['name']
		#print thisTagPath, ' enabled: ', tag.get('enabled', True)
		if tag.get('enabled', True):			
			if 'alarms' in tag:
				for alarm in tag['alarms']:
					if alarm.get('enabled', True) and alarm['name'] != 'EXAMPLE' and str(alarm.get('priority')) != 'Diagnostic':
						alarms.append({'alarmName':alarm['name'],
									   'tagParentPath': parentFolder,
									   'tagName': thisTagPath
									  }
									 )
			if 'tags' in tag:
				alarms.extend(getAlarmsFromFolder(pathFilter, tag['tags'], thisTagPath))
	
	return alarms



				


