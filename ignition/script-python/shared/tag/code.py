LIBRARY = 'shared.tag'
VERSION = '1.1'
LASTUPDATED = '2023-06-22'
LOGGER = system.util.getLogger('SAGE-Scripting-{}'.format(LIBRARY))
from java.lang.System import nanoTime
import traceback

## Yuck, don't use this. I think I wrote this years ago (literally) before system.tag.browse worked recursively!! this function is REALLY slow
#def browseTags(path, filter={}, recursive=False, ret=None):
#	if ret==None: ret=[]
#	# First, browse for anything that can have children (Folders and UDTs, generally)
#	if str(path).find("[") == -1:
#		path = '[default]' + str(path)
#	if recursive:
#		results = system.tag.browse(path)
#		if results.getResults() is not None:
#			for branch in results.getResults():    
#				if branch['hasChildren']:
#					# If something has a child node, then call this function again so we can search deeper.
#					# Include the filter, so newer instances of this call will have the same filter.
#					ret = browseTags(path=branch['fullPath'], filter=filter, recursive=recursive,ret=ret)
#	
#	# Call this function again at the current path, but apply the filter.
#	results = system.tag.browse(path, filter)
#	if results.getResults() is not None:
#		for result in results.getResults():
#			ret.append(result)
#	return ret
	
import java
LIBRARY = 'shared.tag'
def writeBlocking(tagPaths, values, timeout=None):
	fn = '{}.writeBlocking'.format(LIBRARY)
	
	try:
		now = system.date.now()
		ret = system.tag.writeBlocking(tagPaths, values, timeout)
		
		def writeLog():
			if isinstance(newValue, bool):
				actionValue = {True: 'true', False: 'false'}[newValue]
			elif isinstance(newValue, java.util.Date):
				actionValue = system.date.format(newValue, 'yyyy-MM-dd HH:mm:ss.ms')
			else:
				actionValue = str(newValue)
			
			system.util.audit(
							  action            = 'tag write',
							  actionTarget      = tagPath,
							  actionValue       = actionValue,
							  eventTimestamp    = now
							 )
		
		if type(tagPaths) in (list, tuple): 
			for tagPath, newValue in zip(tagPaths, values):
				writeLog()          
		else:
			tagPath = tagPaths
			newValue = values
			
			writeLog()
		return ret
	
	except:
		import traceback
		system.perspective.print('{}: Error occurred writing to tag(s)\r\n{}'.format(fn, traceback.format_exc()))
		raise
	
def writeAsync(tagPaths, values, callback=None):
	fn = '{}.writeAsync'.format(LIBRARY)
	
	try:
		now = system.date.now()
		system.tag.writeAsync(tagPaths, values, callback)
		
		def writeLog():
			if isinstance(newValue, bool):
				actionValue = {True: 'true', False: 'false'}[newValue]
			elif isinstance(newValue, java.util.Date):
				actionValue = system.date.format(newValue, 'yyyy-MM-dd HH:mm:ss.ms')
			else:
				actionValue = str(newValue)
			
			system.util.audit(
							  action            = 'tag write',
							  actionTarget      = tagPath,
							  actionValue       = actionValue,
							  eventTimestamp    = now
							 )
		
		if type(tagPaths) in (list, tuple):
			for tagPath, newValue in zip(tagPaths, values):
				writeLog()          
		else:
			tagPath = tagPaths
			newValue = values
			
			writeLog()
		
	except:
		import traceback
		system.perspective.print('{}: Error occurred writing to tag(s)\r\n{}'.format(fn, traceback.format_exc()))
	raise


class TagReadException(Exception):
	pass

class TagWriteException(Exception):
	pass

class TagWriter:
	""" Simplifies writing to multiple tagpaths  """
	def __init__(self, tagpaths=None, values=None):
		if tagpaths is None:
			self.tagPathsToWrite = []
			self.tagValsToWrite = []
		else:
			self.tagPathsToWrite = list(tagpaths) if isinstance(tagpaths, (list, tuple, set)) else [tagpaths]
			self.tagValsToWrite = list(values) if isinstance(tagpaths, (list, tuple, set)) else [values]
	
		
	def add(self, tagpaths, values):
		if isinstance(tagpaths, (list, tuple)):
			self.tagPathsToWrite.extend(tagpaths)
			self.tagValsToWrite.extend(values)
		elif isinstance(tagpaths, (unicode, str)):
			self.tagPathsToWrite.append(tagpaths)
			self.tagValsToWrite.append(values)
		else:
			raise IllegalArgumentException('Invalid args passed. These must either be lists, tuples, or single string and value.')
	
	
	def __str__(self):
		return '\r\n'.join(['{} -> {}'.format(tagpath, value) for tagpath, value in zip(self.tagPathsToWrite, self.tagValsToWrite)])
	
	
	def __repr__(self):
		return 'TagWriter({}, {})'.format(self.tagPathsToWrite, self.tagValsToWrite)
	
	
	def write(self, removeSuccessful=True, skipFunctionLog=False):
		if len(self.tagPathsToWrite) > 0:
			results = system.tag.writeBlocking(self.tagPathsToWrite, self.tagValsToWrite)
			
			try:
				if not skipFunctionLog:
					shared.util.diag.log_function_call(LIBRARY, 'TagWriter.write', tags={tagpath: {'value': value, 'quality': str(result)} for tagpath, value, result in zip(self.tagPathsToWrite, self.tagValsToWrite, results)})
				pass
			except:
				LOGGER.error('TagWriter: Failed to record to function call log. {}'.format(traceback.format_exc()))
				pass
			
			if removeSuccessful:
				remove_indices = set(i for i, result in enumerate(results) if result.good)
				self.tagPathsToWrite = [tagpath for i, tagpath in enumerate(self.tagPathsToWrite) if i not in remove_indices]
				self.tagValsToWrite = [val for i, val in enumerate(self.tagValsToWrite) if i not in remove_indices]
				results = [result for i, result in enumerate(results) if i not in remove_indices]
			
			if any(not result.good for result in results):
				raise TagWriteException('Failed to write to tag(s):\r\n{}'.format('\r\n'.join(['"{}" ==> {}'.format(tagpath, result) for tagpath,result in zip(self.tagPathsToWrite, results) if not result.good])))
			
		return True