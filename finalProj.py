import mysql.connector
import config
import getpass

#buyer side can see and delete the listing, and listing gets removed from tables.

def main():
	try: 
		usr = config.mysql['user']
		pwd = config.mysql['password']
		hst = config.mysql['host']
		dab = 'TextbookSellingDB'
		
		#create connection
		con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=dab)						  
		#rs = con.cursor()
		rs = con.cursor(buffered=True)
		
		userOptions(con, rs)
		
	except mysql.connector.Error as err:
		print(err)
		
def userOptions(con, rs):
	print
	print("1. Login")
	print("2. Create Account")
	print("3. Exit")
	usrinput = raw_input("Enter your selection: ")
	
	if usrinput == '2' or usrinput == '2 ':
		createAccount(con, rs)
	elif usrinput == '1' or usrinput == '1 ':
		username = raw_input("\tEnter username: ")
		password = getpass.getpass(prompt='\tEnter password: ', stream=None)
		
		validLogin = False
		query = '''SELECT * 
				   FROM Users '''
		rs.execute(query)
		for(a,b,c) in rs:
			user = '{}'.format(a)
			passd = '{}'.format(b)
			if username == user and passd == password:
				validLogin = True
				print
				print("Hello, " + c)
				print
				buyerSellerOptions(con, rs, username)

		if not validLogin:
			print
			print("\tThe username or password entered is incorrect")	
			userOptions(con, rs)
	elif usrinput == '3' or usrinput == '3 ':
		exit()
	else:
		print
		print("\tError: Invalid input")
		print
		userOptions(con,rs)

def buyerSellerOptions(con, rs, username):
	print("Continue as a:")
	print("  1. Seller")
	print("  2. Buyer")
	print("  3. Exit")
	userInput = raw_input("Enter your selection: ")
			
	if userInput == '1' or userInput == '1 ':
		sellerFound = False;
		sellerCheck = ('SELECT * FROM Seller ')
		rs.execute(sellerCheck)
		
		for(a,b) in rs:
			usr = '{}'.format(a)
			if usr == username:
				sellerFound = True;
		if not sellerFound:
			insert = ('INSERT INTO Seller(username) VALUES (%s)')
			rs.execute(insert, (username,))
			con.commit()
			
		query = '''SELECT s.seller_id
					FROM Seller s, Users u
					WHERE u.username = s.username'''
					
		rs.execute(query)
		
		for (a) in rs:
			sellerID = a
		
		sellerID = str(sellerID)
		sellerID = sellerID.replace("(", "")
		sellerID = sellerID.replace(",)", "")
		sellerMenuDisplay(con,rs, sellerID)
		
	elif userInput == '2' or userInput == '2 ':
		buyerFound = False;
		query = ('SELECT * FROM Buyer')
		rs.execute(query)
		
		for (a,b) in rs:
			usr = '{}'.format(b)
			if username == usr:
				buyerFound = True;
		if not buyerFound:
			insert = ('INSERT INTO Buyer(username) VALUES (%s)')
			rs.execute(insert, (username,))
			con.commit()
		
		query = '''SELECT b.buyer_id
					FROM Buyer b, Users u
					WHERE u.username = b.username'''
					
		rs.execute(query)
		
		for (a) in rs:
			buyerID = a
		
		buyerID = str(buyerID)
		buyerID = buyerID.replace("(", "")
		buyerID = buyerID.replace(",)", "")
		buyerMenuDisplay(con, rs, buyerID)
			
	elif userInput == '3' or userInput == '3 ':
		exit()
	else:
		print
		print("\tError: Invalid input")
		print
		buyerSellerOptions(con, rs, username)

def createAccount(con, rs):
	print
	username = raw_input("\tCreate a username (ie. jdoe): ")
	
	#check if user name already exists
	check = '''SELECT *
				FROM Users '''
	rs.execute(check)
	
	isFound = False
	
	for (a,b,c) in rs:
		usr = '{}'.format(a)
		if username == usr:
			isFound = True;
	if not isFound:
		password = getpass.getpass(prompt='\tCreate a password: ', stream=None)
		name = raw_input("\tEnter name: ")	
		insert = '''INSERT INTO Users(username, password, name) VALUES (%s, %s, %s)'''
		rs.execute(insert, (username, password, name))
		con.commit()
			
		print
		print("\tYour account has been created")
	else:
		print
		print("\tThis username is being used in another account")
	userOptions(con, rs)
	
def buyerMenuDisplay(con, rs, buyerID):
	print
	print("Your Menu:")
	print("  1. Search Textbooks")
	print("  2. Search Classes")
	print("	 3. Search Class Textbooks")
	print("	 4. Search Textbook Listings")
	print("	 5. Exit")
	menuChoice = input("Enter your choice: ")
	
	if menuChoice == 1:
		searchTextbooks(con, rs, buyerID)
	elif menuChoice == 2:
		searchClasses(con, rs, buyerID)
	elif menuChoice == 3:
		searchClassTextbooks(con, rs, buyerID)
	elif menuChoice == 4:
		searchListings(con, rs, buyerID)
	elif menuChoice == 5:
		exit()
	else:
		print
		print("\tPlease enter a viable option (1-4)")
		buyerMenuDisplay(con, rs, buyerID)
		
def searchTextbooks(con, rs, buyerID):
	print
	print("Search Textbooks")
	print("Please enter the following information")
	ISBN = input("Enter the ISBN 13 number: ")
	#validate ISBN
				 
	searchTxt = ('SELECT t.title, t.author, t.ISBN, t.edition, t.price '
				 'FROM Textbook t '
				 'WHERE t.ISBN = %s')
	print
	rs.execute(searchTxt,(ISBN,))
        row = rs.fetchone()

	if row is not None:
	 	result = '"{}", By: {}, ISBN: {}, ed.{}, ${}'.format(row[0],row[1],row[2],row[3],row[4])
		print(result)
        else:
            print("There are no textbooks found that match ISBN {}".format(ISBN))
	print
	buyerMenuDisplay(con,rs, buyerID)
	
def searchClasses(con, rs, buyerID):
	print
	print("Search class")
	crn = raw_input("CRN: ")
	#validate CRN

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
	buyerMenuDisplay(con,rs, buyerID)

def searchClassTextbooks(con, rs, buyerID):
	print
	print("Search Class Textbooks")
	crn = input("CRN: ")
	#validate CRN
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
	buyerMenuDisplay(con, rs, buyerID)	

def searchListings(con, rs, buyerID):
	print
	print("Search Textbook Listings")
	print("Please enter the following information")
	textbookTitle = raw_input("Enter the textbook title: ")
	#validate Title	

	query = '''SELECT u.name, t.title, l.price, l.book_condition
				    FROM Seller s, Listing l, Textbook t, Users u
				    WHERE s.seller_id = l.seller_id 
					AND u.username = s.username
				    AND l.ISBN = t.ISBN 
					AND l.listing_state = 'Public'
				    AND t.title = %s '''
				  
	rs.execute(query, (textbookTitle,))
	print
	for (a,b,c,d) in rs:
		result = '{}, {}, {}, {}'.format(a,b,c,d)
		print(result)
	print
	
	searchListingsMenu(con, rs, textbookTitle, buyerID)
	
def searchListingsMenu(con, rs, textbookTitle, buyerID):
	print
	print("Here are some options for seller results: ")
	print("  1. Sort the sellers from lowest to highest price")
	print("  2. Sort the sellers from highest to lowest price")
	print("  3. Request a textbook from a seller")
	print("  4. Find textbook within a price range")
	print("  5. Find listings for another title")
	print("  6. Exit")
	print
	userChoice = input("Enter what option you want: ")
	if userChoice == 1:
		SearchSell = ('SELECT u.name, t.title, l.price '
					  'FROM Users u, Seller s, Listing l, Textbook t '
					  'WHERE s.seller_id = l.seller_id AND l.ISBN = t.ISBN '
					  'AND u.username = s.username '
					   "AND l.listing_state = 'Public' "
					  'AND t.title = %s '
					  'ORDER BY l.price')
					  
		rs.execute(SearchSell, (textbookTitle,))
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	elif userChoice == 2:
		SearchSell = ('SELECT U.name, T.title, L.price '
					  'FROM Users U, Seller S, Listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id '
					  'AND U.username = S.username '
					  'AND L.ISBN = T.ISBN '
					  "AND L.listing_state = 'Public' "
					  'and T.title = %s '
					  'ORDER BY L.price DESC ')
					  
		rs.execute(SearchSell, (textbookTitle,))
		
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	elif userChoice == 3:
		requestTextbook(con, rs, buyerID, textbookTitle)
	elif userChoice == 4:
		lowPrice = input("\tEnter the low end of your price range: ")
		highPrice = input("\tEnter the high end of your price range: ")
		SearchSell = ('SELECT u.name, T.title, L.price '
					  'FROM Users u, Seller S, Listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id AND L.ISBN = T.ISBN '
					   "AND L.listing_state = 'Public' "
					  'and u.username = S.username '
					  'and T.title = %s AND L.price > %s AND L.Price < %s')
					  
		rs.execute(SearchSell, (textbookTitle, lowPrice, highPrice))
		
		print
		for (a,b,c) in rs:
			result = '{}, {}, {}'.format(a,b,c)
			print(result)
		print
	elif userChoice == 5:
		searchListings(con, rs, buyerID)
	elif userChoice == 6:
		exit()
	else:
		print("Please enter a valid choice (1-4)")
		searchListingsMenu(con, rs, textbookTitle, buyerID)

	searchListingsMenu(con,rs,textbookTitle, buyerID)
	
def requestTextbook(con, rs, buyerID, textbookTitle):
	print
	sellerReq = raw_input("Enter seller name you wish to request book from: ")

	#validate the sellerReq
	
	findListing = ('Select L.listing_id, S.seller_id '
		       'FROM Listing L, Seller S, Textbook T, Users U '
		       'WHERE T.title = %s '
		       'AND T.ISBN = L.ISBN '
		       'AND L.seller_id = S.seller_id '
			   'AND U.username = S.username '
		       'AND U.name = %s')

	rs.execute(findListing, (textbookTitle,sellerReq))

	row = rs.fetchone()
	list_id = row[0]
	sell_id = row[1]	

	#add a new row and increment in the request table
	insertReq = 'INSERT INTO Request(request_id, date_requested, request_state, listing_id, seller_id, buyer_id) VALUES(%s, %s, %s, %s, %s, %s)'
	rs.execute(insertReq, (1, '2018-12-02','Pending',list_id,sell_id, buyerID))
	con.commit()	
	
	print("Book has been requested, returning to main menu")
	buyerMenuDisplay(con, rs, buyerID)


#-------------------------------------------------------------------#
#Below is seller options, above is buyer options
#-------------------------------------------------------------------#

# this function will get the seller id and call function to display seller menu
def sellerOption(con, rs):
        sellerID = input("Please enter your seller ID: ")
        sellerMenuDisplay(con, rs, sellerID)
	#start here on seller stuff, this is right when they enter 1 at the start
	print

#this function displays the menu for the seller's options
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
        sellerMenuDisplay(con, rs, sellerID)
    elif sellerMenuChoice == 4:
         seeTextbookRequests(con, rs, sellerID)
         sellerMenuDisplay(con, rs, sellerID)
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

# this function is called when the seller wants to see the requests from buyers
# for their textbook
def seeTextbookRequests(con,rs,sellerID):
    print("See Textbook Requests")
    query = '''SELECT r.date_requested as date_requested, r.request_state as request_state, b.name as buyer_name
               FROM Request r JOIN Buyer b USING (buyer_id)
               WHERE seller_id = %s
			'''
    rs.execute(query,(sellerID,))
    print("Date Requested, Request State, Buyer Name")
    for(date_requested, request_state, buyer_name) in rs:
        print '{} {} {}'.format(date_requested, request_state, buyer_name)
if __name__ == '__main__':
	main()
