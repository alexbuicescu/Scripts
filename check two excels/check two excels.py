class Person(object):

	__cnp_column_index = 0
	__name_column_index = 1
	__summ_column_index = 2
	__account_column_index = 3

	def __init__(self, cnp = 'empty', name = 'empty', summ = 'empty', account = 'empty', excelColumn = []):
		if excelColumn != None and len(excelColumn) == 4:
			self.__cnp = excelColumn[self.__cnp_column_index]
			self.__name = excelColumn[self.__name_column_index]
			self.__summ = excelColumn[self.__summ_column_index]
			self.__account = excelColumn[self.__account_column_index]
		else:
			self.__cnp = cnp
			self.__name = name
			self.__summ = summ
			self.__account = account

		self.__removed = False

	def __eq__(self, other):
		if self.__cnp == other.__cnp and self.__name != other.__name:
			print 'wrong name ' + self.__cnp + ' ' + self.__name + ' ' + other.__name
		return self.__cnp == other.__cnp and self.__summ == other.__summ and self.__account == other.__account

	def __str__(self):
		return str(self.__cnp) + ' ' + str(self.__account) + ' ' + str(self.__name) + ' ' + str(self.__summ)


	def getCnp(self):
		return self.__cnp

	def setCnp(self, cnp):
		self.__cnp = cnp

	cnp = property(getCnp, setCnp)


	def getName(self):
		return self.__name

	def setName(self, name):
		self.__name = name

	name = property(getName, setName)


	def getSumm(self):
		return self.__summ

	def setSumm(self, summ):
		self.__summ = summ

	summ = property(getSumm, setSumm)


	def getAccount(self):
		return self.__account

	def setAccount(self, account):
		self.__account = account

	account = property(getAccount, setAccount)


	def getRemoved(self):
		return self.__removed

	def setRemoved(self, removed):
		self.__removed = removed

	removed = property(getRemoved, setRemoved)


def readExcelFile(excelName):
	excelLines = []
	with open(excelName, 'r') as inputFile:
		for line in inputFile:
			excelLines.append(line)

	excel = ''.join(excelLines)
	return excel

def getListOfPersonsFromFile(inputFile):
	persons = []

	rows = inputFile.split('\n')

	for row in rows:
		columns = row.split('\t')
		persons.append(Person(excelColumn=columns))

	return persons


def readExcels():
	firstExcel = readExcelFile('excel1.txt')
	firstPersons = getListOfPersonsFromFile(firstExcel)

	secondExcel = readExcelFile('excel2.txt')
	secondPersons = getListOfPersonsFromFile(secondExcel)

	for firstPerson in firstPersons:
		for secondPerson in secondPersons[:]:
			if firstPerson == secondPerson:
				secondPersons.remove(secondPerson)
				break

	if len(secondPersons) > 0:
		for secondPerson in secondPersons:
			print secondPerson
	else:
		print 'equal excels'

def run():
	readExcels()

run()