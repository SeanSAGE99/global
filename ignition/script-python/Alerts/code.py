def showAlert(state
			,title
			,message
			,showCloseBtn
			,btnTextPrimary
			,btnTextSecondary
			,btnIconPrimary
			,btnIconSecondary
			,btnIconAlignment
			,btnActionPrimary
			,btnActionSecondary
			,btnActionClose
			,dropdownOptions = []
			,showTextInput=False
			,id="alertDialog"
			):
	import traceback
	try:
		params = {
				"state":state
				,"title":title
				,"message":message
				,"showCloseBtn":showCloseBtn
				,"btnTextPrimary":btnTextPrimary
				,"btnTextSecondary":btnTextSecondary
				,"btnIconPrimary":btnIconPrimary
				,"btnIconSecondary":btnIconSecondary
				,"btnIconAlignment":btnIconAlignment
				,"btnActionPrimary":btnActionPrimary
				,"btnActionSecondary":btnActionSecondary
				,"btnActionClose":btnActionClose
				,"showTextInput":showTextInput
				,"dropdownOptions":dropdownOptions
				,"id":id
				}
		system.perspective.openPopup(id=id
									,view="Shared/General/Popups/Alerts/alert"
									,params=params
									,showCloseIcon=False
									,draggable=False
									,resizable=False
									,modal=True
									,overlayDismiss=True
									,btnActionPrimary="closePopup"
									)
	except Exception,e:
		tb = traceback.format_exc()
		print tb
