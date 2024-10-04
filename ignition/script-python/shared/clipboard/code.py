### Library Revision: 1.0		Increment with any change to the functions within

def writeText(text):
	
	from java.awt.datatransfer import StringSelection
	from java.awt.datatransfer import Clipboard
	from java.awt import Toolkit 
	
	toolkit = Toolkit.getDefaultToolkit()
	clipboard = toolkit.getSystemClipboard()
	clipboard.setContents(StringSelection(text), None)
	
def readText():
	from java.awt.datatransfer import DataFlavor
	contents = clipboard.getContents(None)
	return contents.getTransferData(DataFlavor.stringFlavor)