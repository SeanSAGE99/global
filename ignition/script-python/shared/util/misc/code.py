### Library Revision: 1.0		Increment with any change to the functions within
### Revision History
### No.		Author			Date		Comment
### 1.0		Nick Minchin	2018-11-27	Original
### 1.1		Nick Minchin	2019-07-16	Added findLike function

# check if argument is numeric or not
# return boolean
def isNumeric(s):
	try:
		float(s)
		return True
	except TypeError:
		return False
	except ValueError:
		return False

def getBit(value, bitNumber):
			return value >> bitNumber & 1
			
def findLike(searchString, searchTerm, caseSensitive = 1):
	'''
	Description:
		Searches the search string for the search term, similar in function to the SQL 'LIKE' operator.
		Accepts wildcards % (any characters) and _ (any single character).
		If searchTerm does not contain surrounding wildcards, the start and end characters in both the searchString and searchTerm must match to produce a match.
	Usage:
shared.util.misc.findLike(searchString, searchTerm)

	Example: 
		shared.util.misc.findLike('Hello World', searchTerm)
	'''
	if not caseSensitive:
		searchString = searchString.lower()
		searchTerm = searchTerm.lower()
	
	import re #regex
	# create the regex match string. Need the start and end characters added "^" and "$" as these anchor the match to the start and end of the string.
	# Without these, matches would be found in the middle of the search string surrounded by other characters even if there is no % or _ character at either end.
	# Also, replace SQL % and _ with equivalent regex search terms, .* and .
	
	#TODO should use re.escape to escape regex special characters used in searchTerm... not sure how to use just yet though
	re_match_string = "^" + searchTerm.replace("%",".*").replace("_",".") + "$"
	# if we replaced wildcard characters that were marked to be escaped (e.g. using [] brackets, then replace these back.
	re_match_string = re_match_string.replace("[.*]", "[%]").replace("[.]", "[_]")
	search_re = re.compile(re_match_string)
	
	return 1 if not search_re.match(searchString) is None else 0