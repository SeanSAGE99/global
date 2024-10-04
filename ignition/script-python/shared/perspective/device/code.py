def openDevicePopup(self, event):
	"""
	Description:
	Opens up the standard device popup and sizes it according to the typeId of the device using the lookup table tag.
	"""
	controlEnable =  self.view.params.controlEnable
	deviceParentPath = self.view.params.deviceParentPath
	deviceName = self.view.params.deviceName
	popupID = 'device-popup-%s-%s' % (deviceParentPath, deviceName)
	
	popupHeightDefault = 500
	popupHeight = popupHeightDefault
	try:
		TypeId = system.tag.readBlocking([deviceParentPath + '/' + deviceName + '.typeId'])[0].value
		UDTLookupData = system.dataset.toPyDataSet(system.tag.readBlocking(['[default]System/Datasets/UDTPopupPaths_Perspective'])[0].value)
		for i, row in enumerate(UDTLookupData):
			if row['UDTParentType'] == TypeId:
				popupHeight = row['PopupHeight']
				break
	except:
		pass
	
	system.perspective.print('popupHeight: {}'.format(popupHeight if popupHeight != 0 else '<default>'))
	
	if popupHeight == 0:
		popupHeight = popupHeightDefault
	
	position = {'left':event.clientX
			   ,'height':popupHeight}
	if event.clientY >= popupHeight:
		# a bit dodgy but it's the best we can do without knowing the viewport dimensions...
		position['top'] = event.clientY - popupHeight
	else:
		position['top'] = event.clientY
	
	system.perspective.openPopup(id=popupID,
								 view='_General/Templates/Devices/Control/Device Popup Individual'
								 ,params={'controlEnable':controlEnable
										 ,'deviceParentPath':deviceParentPath
										 ,'deviceName':deviceName
										 ,'popupId': popupID
										 ,'popupHeight': popupHeight}
								 ,position=position
								 ,showCloseIcon=True
								 ,draggable=True
								 ,viewportBound=True
								 )