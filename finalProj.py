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
			sellerOption(con,rs)
		elif userInput == 2:
			buyerOption(con,rs)
		
	except mysql.connector.Error as err:
		print(err)

	
def buyerOption(con, rs):
	buyerID = input("Input your buyer ID: ")
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
        row = rs.fetchone()
        if row is not None:
	    for (a,b,c,d,e) in rs:
		    result = '"{}", By: {}, ISBN: {}, ed.{}, ${}'.format(a,b,c,d,e)
		    print(result)
        else:
            print("There are no textbooks found that match ISBN {}".format(ISBN))
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

# this function will get the seller id and call function to display seller menu
def sellerOption(con, rs):
        sellerID = input("Please enter your seller ID: ")
        sellerMenuDisplay(con, rs, sellerID)
	#start here on seller stuff, this is right when they enter 1 at the start
	print
def sellerMenuDisplay(con, rs, sellerID):
    print
    print("Your Menu:")
    print("1. See my textbooks on sale")
    print("2. Hide a textbook listing")
    print("3. Add a textbook listing")
    print("4. See requests for textbooks")
    print("5. Exit")
    sellerMenuChoice = input("Enter an option from the menu (1-5): ")

    if sellerMenuChoice == 1:
        seeTextbooksOnSale(con, rs, sellerID)
        sellerMenuDisplay(con, rs, sellerID)
    elif sellerMenuChoice == 2:
        hideTextbookListing(con, rs, sellerID)
        sellerMenuDisplay(con, rs, sellerID)
    elif sellerMenuChoice == 3:
        addTextbookListing(con, rs, sellerID)
    elif sellerMenuChoice == 4:
         print(4)
    elif sellerMenuChoice == 5:
        exit()
    else:
        print("\nPlease enter a viable option (1-5)")
        sellerMenuDisplay(con, rs, sellerID)

# when a seller selects a '1' form the menu, they will be able to see their textbooks currently on sale
def seeTextbooksOnSale(con,rs,sellerID):
    print("These are your textbooks on sale: ")
    query = '''SELECT t.title as title, t.ISBN as ISBN, t.author as author, l.date_listed as date_listed, l.price as price, l.book_condition as book_condition
            FROM Listing l JOIN Seller s USING (seller_id) JOIN Textbook t USING (ISBN)
            WHERE seller_id = %s AND l.listing_state = 'Public';
            '''
    rs.execute(query, (sellerID,))
    
    print("Title, ISBN, Author, Date Listed, Price, Condition")
    for(title, ISBN, author, date_listed, price, book_condition) in rs:
        print '{}, {}, {}, {}, ${}, {}'.format(title, ISBN, author, date_listed, price, book_condition)

# when  a seller selects '2' from the menu, they will be able to hide a listing from the public
def hideTextbookListing(con,rs,sellerID):
    print("Hide a Textbook Listing")
    print("Here are your current public listings:")
    query = '''SELECT listing_id, ISBN, CRN, date_listed, price, book_condition
               FROM Listing l
               WHERE l.seller_id = %s AND l.listing_state = 'Public';
            '''
    rs.execute(query, (sellerID,))
    
    # display all of the seller's current public listings
    print("Listing No., ISBN, CRN, Date Listed, Price, Condition")
    for(listing_id, ISBN, CRN, date_listed, price, book_condition) in rs:
        print '{}, {}, {}, {}, {}, {}'.format(listing_id, ISBN, CRN, date_listed, price, book_condition)

    # ask for the listing id they would like to hide
    listing_id = input('Please enter the listing number you would like to hide: ')
    update = '''UPDATE Listing
                SET listing_state = 'Hidden'
                WHERE seller_id = %s AND listing_id = %s
             '''
    rs.execute(update,(sellerID,listing_id))
    #save the changes to the db
    con.commit()
    print("Your listings have been updated.")

def addTextbookListing(con, rs,sellerID):
    print("Add a textbook listing")
    isbn = input("Please enter the ISBN of the textbook you would like to add: ")
    #TO DO : VALIDATE ISBN 
    crn = input("Please enter the CRN of the course: ")
    #TO DO: validate the CRN
    date_listed = input("Please enter the current date in the format YYYY-MM-DD: ")
    #TO DO: validate the date
    price = input("Please enter the price of the textbook: $")
    print("Here are the options for the book condition: ")
    print("1. Poor")
    print("2. Fair")
    print("3. Good")
    print("4. Very Good")
    print("5. Like New")
    book_cond = ''
    book_cond_num = input("Please enter (1-5) for the book's condition: ")
    if book_cond_num == 1:
        book_cond = 'Poor'
    elif book_cond_num == 2:
        book_cond = 'Fair'
    elif book_cond_num == 3:
        book_cond = 'Good'
    elif book_cond_num == 4:
        book_cond = 'Very Good'
    elif book_cond_num == 5:
        book_cond = 'Like New'
    else:
    #TO DO: ask for user input again if the number is invalid or just store as null
        book_cond = ''
    insert = ''' INSERT INTO Listing(seller_id,ISBN,CRN,date_listed,price,book_condition,listing_state)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    rs.execute(insert,(sellerID,isbn,crn,date_listed,price,book_cond,'Public'))
    con.commit()
    print("You have added a listing!")
if __name__ == '__main__':
	main()
	
