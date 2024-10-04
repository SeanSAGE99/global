from java.net import UnknownHostException

def ping(host, timeout=1000):
	from java.net import InetAddress
	
	try:
		ip = InetAddress.getByName(host)
		r =  ip.isReachable(timeout)
	except UnknownHostException as e:
		r = False
	
	return r
