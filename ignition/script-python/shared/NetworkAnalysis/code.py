def ping(host,timeout):
	from java.net import InetAddress
	ip = InetAddress.getByName(host)
	r =  ip.isReachable(timeout)
	return r
