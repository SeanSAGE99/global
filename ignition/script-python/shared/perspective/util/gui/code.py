#def confirmAction(message, onConfirm_TagPath, onConfirm_WriteValue=1, onCancel_TagPath=None, onCancel_WriteValue=None):
#	system.perspective.openDock('confirm-action')
#	system.perspective.sendMessage('confirm-action', payload={'message':message,
#															  'onConfirm_TagPath':onConfirm_TagPath,
#															  'onConfirm_WriteValue': onConfirm_WriteValue,
#															  'onCancel_TagPath': onCancel_TagPath,
#															  'onCancel_WriteValue': onCancel_WriteValue})


def confirmAction(message, onConfirm_TagPath, onConfirm_WriteValue=1, onCancel_TagPath=None, onCancel_WriteValue=None):
	system.perspective.openPopup(id='confirm-action',
								 view='Shared/General/Popups/ppuConfirmAction',
								 params={'message':message,
										  'onConfirm_TagPath':onConfirm_TagPath,
										  'onConfirm_WriteValue': onConfirm_WriteValue,
										  'onCancel_TagPath': onCancel_TagPath,
										  'onCancel_WriteValue': onCancel_WriteValue},
								 title='Confirm Action',
								 position={'left':'auto',
								 		   'top':'auto'},
								 showCloseIcon=False,
								 draggable=False,
								 modal=True,
								 overlayDismiss=True)