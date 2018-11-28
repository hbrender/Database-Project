import mysql.connector
#import config

def main():
  #  try: 
        # connection info - waiting for information about it from bowers
		
        #usr = config.mysql['user']
        #pwd = config.mysql['password']
        #hst = config.mysql['host']
        #dab = usr + 'DB'
		
		# create a connection
        #con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=dab)
									  
		#rs = con.cursor()
		
	print("Are you:")
	print("  1. Seller")
	print("  2. Buyer")
	userInput = input("Enter your selection: ")
	if userInput == 1:
		sellerOption()
	elif userInput == 2:
		buyerOption()
		
	#except mysql.connector.Error as err:
    #    print(err)

	
def buyerOption():
	buyerID = input("Input your buyerID: ")
	buyerMenuDisplay()
	
def buyerMenuDisplay():
	print
	print("Your Menu:")
	print("1.	Search Textbooks")
	print("2.	Search Classes")
	print("3.	Search Sellers")
	print("4.	exit")
	menuChoice = input("Enter your choice: ")
	
	if menuChoice == 1:
		searchTextbooks()
	elif menuChoice == 2:
		searchClasses()
	elif menuChoice == 3:
		searchSellers()
	elif menuChoice == 4:
		exit()
	else:
		print
		print("Please enter a viable option (1-4)")
		buyerMenuDisplay()
		
def searchTextbooks():
	print
	print("Search Textbooks")
	print("Please enter the following information")
	courseID = input("Enter the course ID (CRN): ")
	textbookTitle = raw_input("Enter the textbook title: ")
	ISBN = input("Enter the ISBN Number (optional): ")
	author = raw_input("Enter the author (optional): ")
	edition = input("Enter the addition (optional): ")	
	#Query the database and output the results
	
def searchClasses():
	print
	print("Search class")
	userClass = input("Course id (CRN): ")
	courseTitle = raw_input("Course title (optional): ")
	instructor = raw_input("Instructor (optional): ")
	#query using group by to return all different books associated with the class
	
def searchSellers():
	print
	print
	print("Search Sellers")
	print("Please enter the following information")
	textbookTitle = raw_input("Enter the textbook title: ")
	ISBN = input("Enter the ISBN: ")
	author = raw_input("Enter the author: ")
	edition = input("Enter the edition: ")
	
	#query and display the sellers of the books
	
#	searchSellerMenu()
	
def searchSellerMenu():
	print
	print("Here are some options for seller results: ")
	print("1.	Sort the sellers from the highest to lowerst prices")
	print("2.	Soft the sellers from lowest to highest prices")
	print("3. Request a textbook from a seller")
	print("4. Find textbook within a price range")
	print
	userChoice = ("Enter what option you want: ")
	if userChoice == 1:
		#query it with the same query except order by
		print
	elif userChoice == 2:
		#^
		print
	elif userChoice == 3:
		requestTextbook()
	elif userChoice == 4:
		#add a where clause to the query
		print
	else:
		print("Please enter a valid choice (1-4)")
		searchSellerMenu()
	
def requestTextbook():
	print
	sellerReq = raw_input("Enter the seller you wish to request this book from: ")
	#are we actually requesting it?
	print("Book has been requested, returning to main menu")
	buyerMenuDisplay()


#-------------------------------------------------------------------#
#Below is seller options, above is buyer options
#-------------------------------------------------------------------#

def sellerOption():
	#start here on seller stuff, this is right when they enter 1 at the start
	print


if __name__ == '__main__':
	main()
	

