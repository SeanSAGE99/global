### Library Revision: 1.0		
### Revision History
### No.		Author				Date		Comment
### 1.0		Tomasz Jankowski	2023-02-16	Original

### Dependencies


def LightsScheduler():
	import traceback
	try:
		hour = system.date.getHour24(system.date.now())
		system.perspective.print(hour)
		data = system.db.runNamedQuery('lights scheduler/Select All DBs')
		
		pyTable = system.dataset.toPyDataSet(data)	
		
		
		for row in pyTable:
			if row[4]: # check if scheduler is enbaled for this DB
				db_name = row[1]
				day = row[5]
				curfew = row[6]
				off_time = row[7]
				on_time = row[8]
				#system.perspective.print(db_name)
				
						
				if hour == off_time:
					light_level = curfew
					system.perspective.print('cufew')
					LightsControl(db_name,light_level)
				elif hour == on_time:
					light_level = day
					system.perspective.print('day')
					LightsControl(db_name,light_level)		
			
	except:
		system.perspective.print(traceback.format_exc())

def LightsControl(db_name,light_level):					

		tags = system.tag.browse('International' or 'Domestic', filter={'tagType':'UdtInstance', 'recursive':True, 'name':'*'+db_name+'*'})
		#system.perspective.print(tags)
				
		if tags: # if tag exist
			tags = [tag['fullPath'] for tag in tags]
			paths  = ['{}/Lights Control/'.format(tag) for tag in tags]
			path = paths[0] + 'Lights 25pct Cmd'
			system.perspective.print(path)
			quality = system.tag.readBlocking(path)[0].quality.isGood()
			system.perspective.print(quality)
			if quality:
				if light_level == 0:
					path = paths[0] + 'Lights Off Cmd'
					system.tag.writeBlocking(path, 1)
					system.perspective.print('Lights Off Cmd')	
				elif 0 <light_level <50:
					path = paths[0] + 'Lights 25pct Cmd'
					system.tag.writeBlocking(path, 1)
					system.perspective.print('Lights 25 Cmd')	
				elif 50 <=light_level <75:
					path = paths[0] + 'Lights 50pct Cmd'
					system.tag.writeBlocking(path, 1)
					system.perspective.print('Lights 50 Cmd')
				elif 75 <=light_level <100:
					path = paths[0] + 'Lights 75pct Cmd'
					system.tag.writeBlocking(path, 1)
					system.perspective.print('Lights 75 Cmd')
				elif light_level == 100:
					path = paths[0] + 'Lights 100pct Cmd'
					system.tag.writeBlocking(path, 1)		
					system.perspective.print('Lights 100 Cmd')	