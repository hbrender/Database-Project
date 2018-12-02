import mysql.connector
import config

#buyer side can see and delete the listing, and listing gets removed from tables.

def main():
	try: 
		usr = config.mysql['user']
		pwd = config.mysql['password']
		hst = config.mysql['host']
		dab = 'TextbookSellingDB'
		
		#create connection
		con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=dab)
										  
		rs = con.cursor()
		
		print("Are you:")
		print("  1. Seller")
		print("  2. Buyer")
		userInput = input("Enter your selection: ")
		if userInput == 1:
			sellerOption()
		elif userInput == 2:
			buyerOption(con,rs)
		
	except mysql.connector.Error as err:
		print(err)

	
def buyerOption(con, rs):
	buyerID = input("Input your buyerID: ")
	buyerMenuDisplay(con, rs)
	
def buyerMenuDisplay(con, rs):
	print
	print("Your Menu:")
	print("1.	Search Textbooks")
	print("2.	Search Classes")
	print("3.   Search Class Textbooks")
	print("5.	Search Sellers")
	print("5.	Exit")
	menuChoice = input("Enter your choice: ")
	
	if menuChoice == 1:
		searchTextbooks(con, rs)
	elif menuChoice == 2:
		searchClasses(con, rs)
	elif menuChoice == 3:
		searchClassTextbooks(con, rs)
	elif menuChoice == 4:
		searchSellers(con, rs)
	elif menuChoice == 5:
		exit()
	else:
		print
		print("Please enter a viable option (1-4)")
		buyerMenuDisplay(con, rs)
		
def searchTextbooks(con, rs):
	print
	print("Search Textbooks")
	print("Please enter the following information")
	ISBN = input("Enter the ISBN 13 number: ")
	#title = raw_input("Enter the textbook title: ")
	#author = raw_input("Enter the author: ")
	#edition = input("Enter the edition: ")
	#publisher = input("Enter the publisher: ")
	#year = input("Enter the year published: ")
	
	searchTxt = ('SELECT t.title, t.author, t.ISBN, t.edition, t.price '
				 'FROM Textbook t '
				 'WHERE t.ISBN = %s')
	print
	rs.execute(searchTxt,(ISBN,))
	print
	
	for (a,b,c,d,e) in rs:
		result = '"{}", By: {}, ISBN: {}, ed.{}, ${}'.format(a,b,c,d,e)
		print(result)
	print
	
def searchClasses(con, rs):
	print
	print("Search class")
	crn = raw_input("CRN: ")
	#dept = raw_input("Department: ")
	#course_num = raw_input("Course Number: ")
	#course_sec = raw_input("Course Section: ")
	#instructor = raw_input("Instructor: ")
	#term = raw_input("Term: ")
	#course_year = raw_input("Year: ")
	print
	
	searchC = ('SELECT c.CRN, c.instructor, c.department, c.course_number, c.course_section, c.term, c.course_year '
	           'FROM Course c '
			   'WHERE c.CRN = %s')
	rs.execute(searchC, (crn,))
	
	print
	for(a,b,c,d,e,f,g) in rs:
		result = 'CRN: {}, {}, {} {}-{}, {} {}'.format(a,b,c,d,e,f,g)
		print(result)
	print

def searchClassTextbooks(con, rs):
	print
	print("Search Class Textbooks")
	crn = input("CRN: ")
	print
	
	searchC = ('SELECT ct.CRN, c.department, c.course_number, c.course_section, c.instructor, t.title, t.ISBN '
	           'FROM CourseTextbook ct, Course c, Textbook t '
			   'WHERE c.CRN = %s '
			   'AND ct.CRN = c.CRN '
			   'AND t.ISBN = ct.ISBN ')
	rs.execute(searchC, (crn,))
	
	print
	for(a,b,c,d,e,f,g) in rs:
		result = '(CRN: {}, {} {}-{}, {}) Required Text: "{}", ISBN: {}'.format(a,b,c,d,e,f,g)
		print(result)
	print
	
def searchSellers(con, rs):
	print
	print
	print("Search Sellers")
	print("Please enter the following information")
	textbookTitle = raw_input("Enter the textbook title: ")
	
	#HERE
	SearchSell = ('SELECT S.name, T.title, L.price '
				  'FROM Seller S, listing L, Textbook T '
				  'WHERE S.seller_id = L.seller_id AND L.textbook_id = T.textbook_id '
				  'and T.title = %s ')
				  
	rs.execute(SearchSell, textbookTitle)
	con.commit()
	print
	for (a,b,c) in rs:
		result = '{}, {}, {}'.format(a,b,c)
		print(result)
	print
	
	searchSellerMenu(con, rs)
	
def searchSellerMenu(con, rs):
	print
	print("Here are some options for seller results: ")
	print("1.	Sort the sellers from the highest to lowest prices")
	print("2.	Sort the sellers from lowest to highest prices")
	print("3.	Request a textbook from a seller")
	print("4.	Find textbook within a price range")
	print
	userChoice = ("Enter what option you want: ")
	if userChoice == 1:
		#query it with the same query except order by
		#HERE
		SearchSell = ('SELECT S.name, T.title, L.price '
					  'FROM Seller S, listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id AND L.textbook_id = T.textbook_id '
					  'and T.title = %s '
					  'ORDER BY T.price')
					  
		rs.execute(SearchSell, textbookTitle)
		con.commit()
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	elif userChoice == 2:
		#HERE
		SearchSell = ('SELECT S.name, T.title, L.price '
					  'FROM Seller S, listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id AND L.textbook_id = T.textbook_id '
					  'and T.title = %s '
					  'ORDER BY T.price DESC ')
					  
		rs.execute(SearchSell, textbookTitle)
		con.commit()
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	elif userChoice == 3:
		requestTextbook(con, rs)
	elif userChoice == 4:
		lowPrice = input("Enter the low end of your price range")
		highPrice = input("Enter the high end of your price range")
		SearchSell = ('SELECT S.name, T.title, L.price '
					  'FROM Seller S, listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id AND L.textbook_id = T.textbook_id '
					  'and T.title = %s AND L.price > %s AND L.Price < %s')
					  
		rs.execute(SearchSell, (textbookTitle, lowPrice, highPrice))
		con.commit()
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	else:
		print("Please enter a valid choice (1-4)")
		searchSellerMenu(con, rs)
	
def requestTextbook(con, rs):
	print
	sellerReq = raw_input("Enter the seller you wish to request this book from: ")
	
	#add a new row in the request table
	#insertReq = 'INSERT INTO Request(request_id, date_requested, requested_state, listing_id, seller_id, buyer_id) VALUES(%s, %s, %s, %s, %s, %s)
	#how do we auto increment with sql again? we should use it for request_id
	#stopped here
	#rs.execute(insertReq,(autoIncrementThing, '2018-04-23', 'pending', )
	
	
	
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
	
