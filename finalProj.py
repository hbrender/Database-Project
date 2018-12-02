import mysql.connector
import config

#buyer side can see and delete the listing, and listing gets removed from tables.

def main():
	try: 
        	usr = config.mysql['user']
        	pwd = config.mysql['password']
        	hst = config.mysql['host']
        	dab = 'TextbookSellingDB'
		
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
	print("3.	Search Sellers")
	print("4.	exit")
	menuChoice = input("Enter your choice: ")
	
	if menuChoice == 1:
		searchTextbooks(con, rs)
	elif menuChoice == 2:
		searchClasses(con, rs)
	elif menuChoice == 3:
		searchSellers(con, rs)
	elif menuChoice == 4:
		exit()
	else:
		print
		print("Please enter a viable option (1-4)")
		buyerMenuDisplay(con, rs)
		
def searchTextbooks(con, rs):
	print
	print("Search Textbooks")
	print("Please enter the following information")
	courseID = input("Enter the course ID (CRN): ")
	textbookTitle = raw_input("Enter the textbook title: ")
	ISBN = input("Enter the ISBN Number (optional): ")
	author = raw_input("Enter the author (optional): ")
	edition = input("Enter the addition (optional): ")	
	
	#HERE
	searchTxt = ('SELECT T.title, T.author, T.ISBN, T.edition, L.price '
		  'FROM CourseTextbook CT, Textbook T, Listing L '
		 'WHERE CT.textbook_id = T.textbook_id and L.textbook_id = T.textbook_id ' 
		        'and CT.CRN = %s and T.title = %s ')
	print
	rs.execute(searchTxt,(courseID,textbookTitle))
	con.commit()
	print
	for (a,b,c,d,e) in rs:
		result = '{}, {}, {,} {}, ${}'.format(a,b,c,d,e)
		print(result)
	print
	
def searchClasses(con, rs):
	print
	print("Search class")
	userClass = input("Course id (CRN): ")
	courseTitle = raw_input("Course title (optional): ")
	instructor = raw_input("Instructor (optional): ")
	print
	
	#HERE
	searchC = ('SELECT CT.CRN, C.instructor, T.title, T.ISBN '
	            'FROM CourseTextbook CT, Course C, Textbook T '
				'WHERE C.CRN = %s and CT.CRN = C.CRN and T.textbook_id = CT.textbook_id ')
	rs.execute(searchC, userClass)
	con.commit()
	print
	for(a,b,c,d) in rs:
		result = '{}, {}, {}, {}'.format(a,b,c,d)
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
	insertReq = 'INSERT INTO Request(request_id, date_requested, requested_state, listing_id, seller_id, buyer_id) VALUES(%s, %s, %s, %s, %s, %s)
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
	

