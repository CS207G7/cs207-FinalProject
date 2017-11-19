import sqlite3


def getNASACoeff(species, temperature):
	#db = sqlite3.connect("../data/NASA.sqlite")
	db = sqlite3.connect("../data/NASA.sqlite")
	cursor = db.cursor()
	#Check for valid coefficients within temperature range in LOW table
	lowTemp = '''SELECT * FROM LOW WHERE SPECIES_NAME = "{}" \
		AND TLOW <= {} AND THIGH >= {}'''.format(species, temperature, temperature)
	highTemp = '''SELECT * FROM HIGH WHERE SPECIES_NAME = "{}" \
		AND TLOW <= {} AND THIGH >= {}'''.format(species, temperature, temperature)
	output = cursor.execute(lowTemp).fetchall()
	if (len(output) == 0): #Unable to find valid coefficients in LOW table. Check HIGH table.
		output = cursor.execute(highTemp).fetchall()
	if (len(output) == 0):
		#Still unable to find coefficients. Either species or temperature is invalid.
		cursor.close()
		raise Exception("Unable to find valid NASA coefficients for {} at {}".format(species, temperature))

	cursor.close()
	return list(output[0])[3:]