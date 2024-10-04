def getTotalSecondsToStr(totalSeconds):
	hours = str(int(totalSeconds /60/60))
	mins = ("00" + str(int(totalSeconds/60 % 60)))[-2:]
	secs = ("00" + str(int(totalSeconds%60)))[-2:]
	
	ret = hours + ":" + mins + ":" + secs
	
	return ret