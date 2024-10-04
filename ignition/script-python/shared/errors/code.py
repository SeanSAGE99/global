def sendExceptionEmail(functionPath, e):
	import traceback
	error = traceback.format_exc()
	fromAddr = 'ams@syd.com.au'
	subject = 'AMS Ignition Error!'
	to = ['tomasz.jankowski@gotosage.com']
	body = 'Function: %s()\n\nError Traceback:\n'%(functionPath) + error
	system.net.sendEmail(smtpProfile='TWE Email', fromAddr=fromAddr, subject=subject, body=body, to=to)

def sendEmail(subject, body):
	fromAddr = 'ams@syd.com.au'
	to = ['tomasz.jankowski@gotosage.com']
	try:
		system.net.sendEmail(smtpProfile='AMS', fromAddr=fromAddr, subject='AMS IGNITION - ' + subject, body=body, to=to)
	except: pass