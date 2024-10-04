import datetime
import math

def getJulianDatetime(date):
    """
    Convert a datetime object into julian float.
    Args:
        date: datetime-object of date in question

    Returns: float - Julian calculated datetime.
    Raises: 
        TypeError : Incorrect parameter type
        ValueError: Date out of range of equation
    """
    # convert Date object to datetime.datetime object, required by this function
    date = datetime.datetime(system.date.getYear(date), system.date.getMonth(date), system.date.getDayOfMonth(date))
    # Ensure correct format
    if not isinstance(date, datetime.datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')
	
    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
                          date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                                  2)) / 24.0 - 0.5 * (
							100 * date.year + date.month - 190002.5) / abs(100 * date.year + date.month - 190002.5) + 0.5
							# math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5 -- copysign not available until Python 2.6 :(
    return julian_datetime

def getOrdinalDate(date):
	return int(str(system.date.getYear(date))[-2:] + str(system.date.getDayOfYear(date)))

def getBottleDate(date):
	year_last_digit = str(system.date.getYear(date))[-2:][-1:]
	day = str(system.date.getDayOfYear(date))
	
	return "L" + year_last_digit + " " + day	


def formatRuntime(totalSecs, format):
	ret = None
	d = int(math.floor(totalSecs/(60*60*24)))
	h = int(math.floor(totalSecs/(60*60)) % 24)
	m = int(math.floor(totalSecs/(60)) % 60)
	s = int(math.floor(totalSecs % 60))
	#print d,h,m,s
	
	if format == 0:
		ret = '{:03d}:{:02d}:{:02d}'.format(d,h,m)
	if format == 1:
		ret = '{} m'.format(m)
		if h > 0:
			ret = '{} h, '.format(h) + ret
		if d > 0:
			ret = '{} d, '.format(d) + ret
		
	if format == 2:
		ret = '{} m'.format(m)
		if h > 0 or d > 0:
			ret = '{} h, '.format(d*24 + h) + ret
	if format == 3:
		ret = '{} h'.format(d*24 + h)
	
	return ret