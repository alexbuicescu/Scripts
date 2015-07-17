months = 240 #the number of months for the credit
paying = 7000 #ron/month
creditSum = 161000 #(ron) total sum borrowed from the bank
interest = 0.0397 #interest to pay monthly
creditRemaining = creditSum

actualMonths = 0
totalInterestSum = 0

while creditRemaining > 0:
	
	currentMonthInterest = creditRemaining * interest * 31.0 / 365.0 #the interest we pay for the current month

	currentSold = paying - currentMonthInterest #the sum we actually pay for the credit

	creditRemaining = creditRemaining - currentSold

	actualMonths += 1
	totalInterestSum += currentMonthInterest

	# print currentMonthInterest, currentSold, creditRemaining
	# print creditRemaining
	print currentMonthInterest

print actualMonths, totalInterestSum

# 4000 monthly
# actual months 62
# total interest 23975.2791579

#abonamente, transport slatina, mancare
130 + 320 + 500