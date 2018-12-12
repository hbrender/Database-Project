import mysql.connector
import config
import getpass
import datetime

#set up the connection to the database and call user options
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
		
# display user options to get username and password
def userOptions(con, rs):
	print
	print("1. Login")
	print("2. Create Account")
	print("3. Exit")
	usrinput = raw_input("Enter your selection: ")
	
	if usrinput == '2' or usrinput == '2 ':
		createAccount(con, rs)
        # if they entered option 1, login
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
                        # if the username and password are valid, call the buyerSellerOptions menu
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

# the program will ask if they want to continue as either a buyer or a seller of textbooks
def buyerSellerOptions(con, rs, username):
	print("Continue as a:")
	print("  1. Seller")
	print("  2. Buyer")
	print("  3. Exit")
	userInput = raw_input("Enter your selection: ")
			
        # try to find the seller associated with a particular username
	if userInput == '1' or userInput == '1 ':
		sellerFound = False;
		sellerCheck = ('SELECT * FROM Seller ')
		rs.execute(sellerCheck)
		
		for(a,b) in rs:
			usr = '{}'.format(b)
			if usr == username:
				sellerFound = True;
		if not sellerFound:
			insert = ('INSERT INTO Seller(username) VALUES (%s)')
			rs.execute(insert, (username,))
			con.commit()
			
		query = '''SELECT s.seller_id
					FROM Seller s, Users u
					WHERE u.username = s.username
			 AND u.username = %s'''
					
		rs.execute(query, (username,))
		
		for (a) in rs:
			sellerID = a
		
		sellerID = str(sellerID)
		sellerID = sellerID.replace("(", "")
		sellerID = sellerID.replace(",)", "")
                # call sellerMenuDisplay to display seller menu options
		sellerMenuDisplay(con,rs, sellerID)
		
        # try to find a buyer associated with a certain username
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
					WHERE u.username = b.username
			AND u.username = %s'''
					
		rs.execute(query, (username,))
		
		for (a) in rs:
			buyerID = a
		
		buyerID = str(buyerID)
		buyerID = buyerID.replace("(", "")
		buyerID = buyerID.replace(",)", "")
                # call buyerMenuDisplay to display buyer menu to the user
		buyerMenuDisplay(con, rs, buyerID)
			
	elif userInput == '3' or userInput == '3 ':
		exit()
	else:
		print
		print("\tError: Invalid input")
		print
		buyerSellerOptions(con, rs, username)

# called if the user wants to create an account
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
        #if username is not found, create password and insert the new user into the User table
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
	
# menu display for options for buyer
def buyerMenuDisplay(con, rs, buyerID):
	print
	print("Your Menu:")
	print("  1. Search Textbooks")
	print("  2. Search Classes")
	print("	 3. Search Class Textbooks")
	print("	 4. Search Textbook Listings")
	print("  5. See your requests " )
	print("  6. see textbooks that don't have a listing")
	print("	 7. Exit")
	try:
		menuChoice = int(raw_input("Enter your choice: "))
	except ValueError:
		print("\n\tOnly enter integer values")
		buyerMenuDisplay(con,rs,buyerID)
	
	if menuChoice == 1:
		searchTextbooks(con, rs, buyerID)
	elif menuChoice == 2:
		searchClasses(con, rs, buyerID)
	elif menuChoice == 3:
		searchClassTextbooks(con, rs, buyerID)
	elif menuChoice == 4:
		searchListings(con, rs, buyerID)
	elif menuChoice == 5:
		seeRequests(con,rs,buyerID)
	elif menuChoice == 6:
		txtNoListing(con,rs,buyerID)
	elif menuChoice == 7:
		exit()
	else:
		print
		print("\tPlease enter a viable option (1-8)")
		buyerMenuDisplay(con, rs, buyerID)

# buyer can view all of the requests that they have made for textbooks
def seeRequests(con,rs,buyerID):
	print
        # find the declined requests
	declined = ('SELECT t.Title,s.username '
		        '  FROM Textbook t JOIN Listing L using(ISBN), Request R, Seller s'
		        ' WHERE R.request_state = "Declined" '
                '	AND	R.buyer_id = %s '
		        '   AND L.listing_id = R.listing_id '
                '   AND	s.seller_id = R.seller_id ')
	rs.execute(declined,(buyerID,))
	print("-------------------")
	print("-Declined Requests-")
	print("-------------------")
	for (a,b) in rs:
		result = 'Textbook: {}, Seller: {}'.format(a,b)
		print(result)
	print

	print
        #find the pending requests
	pending = ('SELECT t.Title,s.username '
		        '  FROM Textbook t JOIN Listing L using(ISBN), Request R, Seller s'
		        ' WHERE R.request_state = "Pending" '
                '	AND	R.buyer_id = %s '
		        '   AND L.listing_id = R.listing_id '
                '   AND	s.seller_id = R.seller_id ')
	rs.execute(pending,(buyerID,))
	print("-------------------")
	print("-Pending Requests-")
	print("-------------------")
	for (a,b) in rs:
		result = 'Textbook: {}, Seller: {}'.format(a,b)
		print(result)
	print

	print
        # find the accepted requests
	accepted = ('SELECT t.Title,s.username '
		        '  FROM Textbook t JOIN Listing L using(ISBN), Request R, Seller s'
		        ' WHERE R.request_state = "Approved" '
                '	AND	R.buyer_id = %s '
		        '   AND L.listing_id = R.listing_id '
                '   AND	s.seller_id = R.seller_id ')
	rs.execute(accepted,(buyerID,))
	print("-------------------")
	print("-Approved Requests-")
	print("-------------------")
        # if a request has been accepted, the buyer will be able to see the seller's contact information
	for (a,b) in rs:
		result = 'Textbook: {}, Seller Email: {}@zagmail.gonzaga.edu'.format(a,b)
		print(result)
	print

	buyerMenuDisplay(con,rs,buyerID)

def txtNoListing(con,rs,buyerID):
        #find the textbooks that do not have any listings 
	outerQ = ('SELECT T.title, T.ISBN '
		  'FROM Textbook T LEFT JOIN Listing L USING (ISBN) '
		  'WHERE L.ISBN is NULL')

	print
	rs.execute(outerQ)
	for (a,b) in rs:
		result = 'Textbook: {}, ISBN: {}'.format(a,b)
		print(result)
	buyerMenuDisplay(con,rs,buyerID)
	
# called when the buyer wants to look for a textbook
def searchTextbooks(con, rs, buyerID):
	print
	print("Search Textbooks")
	print("Please enter the following information")
	try:
		ISBN = int(raw_input("Enter the ISBN 13 number: "))
	except ValueError:
		print("please only enter numbers")
		searchTextbooks(con,rs,buyerID)
		 
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
	
# called when the buyer wants to look for a particular class at Gonzaga
def searchClasses(con, rs, buyerID):
	print
	isThere = False
	print("Search class")
	try:
		crn = int(raw_input("CRN: "))
	except ValueError:
		print("please only enter integer values")
		searchClasses(con,rs,buyerID)

	print
	
	searchC = ('SELECT c.CRN, c.instructor, c.department, c.course_number, c.course_section, c.term, c.course_year '
	           'FROM Course c '
			   'WHERE c.CRN = %s')
	rs.execute(searchC, (crn,))
	
	print
	for(a,b,c,d,e,f,g) in rs:
		result = 'CRN: {}, {}, {} {}-{}, {} {}'.format(a,b,c,d,e,f,g)
		print(result)
		isThere = True
	print
	if not isThere:
		print("There are currently no classes that match that CRN")
	
	buyerMenuDisplay(con,rs, buyerID)

# look for required textbooks for a particular course
def searchClassTextbooks(con, rs, buyerID):
	print
	isThere = False
	print("Search Class Textbooks")
	try:
		crn = int(raw_input("CRN: "))
	except ValueError:
		print("please only enter integer values")
		searchClasses(con,rs,buyerID)
	print
	
       # search for all textbooks associated with a particular course CRN
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
		isThere = True
	print
	if not isThere:	
		print("There are currently no textbooks listed for that class")
	buyerMenuDisplay(con, rs, buyerID)	

def searchListings(con, rs, buyerID):
	print
	isThere = False
	print("Search Textbook Listings")
	print("Please enter the following information")
	textbookTitle = raw_input("Enter the textbook title: ")
	
	query = '''SELECT l.listing_id, u.name, t.title, l.price, l.book_condition, l.date_listed
				    FROM Seller s, Listing l, Textbook t, Users u
				    WHERE s.seller_id = l.seller_id 
					AND u.username = s.username
				    AND l.ISBN = t.ISBN 
					AND l.listing_state = 'Public'
				    AND t.title = %s '''
				  
	rs.execute(query, (textbookTitle,))
	print
	for (a,b,c,d,e,f) in rs:
		result = 'Listing ID: {}, Seller: {}, {}, ${}, Condition: {}, Date Posted: {}'.format(a,b,c,d,e,f)
		print(result)
		isThere = True
	print
	if not isThere:
		print("You have entered a book that doesn't have any listings")
		buyerMenuDisplay(con,rs,buyerID)
	searchListingsMenu(con, rs, textbookTitle, buyerID)
	
def searchListingsMenu(con, rs, textbookTitle, buyerID):
	print
	print("Here are some options for seller results: ")
	print("\t1. Sort the sellers from lowest to highest price")
	print("\t2. Sort the sellers from highest to lowest price")
	print("\t3. Request a textbook from a seller")
	print("\t4. Find textbook within a price range")
	print("\t5. Find listings for another title")
	print("\t6. Find the lowest priced book")
	print("\t7. Exit")
	print
	try:
		userChoice = int(raw_input("Enter what option you want: "))
	except ValueError:
		print("only enter integers here")
		searchListingsMenu(con,rs,textbookTitle,buyerID)
	if userChoice == 1:
		SearchSell = ('SELECT l.listing_id, u.name, t.title, l.price,l.book_condition, l.date_listed '
					  'FROM Users u, Seller s, Listing l, Textbook t '
					  'WHERE s.seller_id = l.seller_id AND l.ISBN = t.ISBN '
					  'AND u.username = s.username '
					   "AND l.listing_state = 'Public' "
					  'AND t.title = %s '
					  'ORDER BY l.price')
					  
		rs.execute(SearchSell, (textbookTitle,))
		print
		for (a,b,c,d,e,f) in rs:
			result = 'Listing ID: {}, Seller: {}, {}, ${}, Condition: {}, Date Posted: {}'.format(a,b,c,d,e,f)
			print(result)
		print
	elif userChoice == 2:
		SearchSell = ('SELECT L.listing_id, U.name, T.title, L.price,L.book_condition, L.date_listed '
					  'FROM Users U, Seller S, Listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id '
					  'AND U.username = S.username '
					  'AND L.ISBN = T.ISBN '
					  "AND L.listing_state = 'Public' "
					  'and T.title = %s '
					  'ORDER BY L.price DESC ')
					  
		rs.execute(SearchSell, (textbookTitle,))
		
		print
		for (a,b,c,d,e,f) in rs:
			result = 'Listing ID: {}, Seller: {}, {}, ${}, Condition: {}, Date Posted: {}'.format(a,b,c,d,e,f)
			print(result)
		print
	elif userChoice == 3:
		requestTextbook(con, rs, buyerID, textbookTitle)
	elif userChoice == 4:
		lowPrice = input("\tEnter the low end of your price range: ")
		highPrice = input("\tEnter the high end of your price range: ")
		SearchSell = ('SELECT L.listing_id, u.name, T.title, L.price, L.book_condition, L.date_listed '
					  'FROM Users u, Seller S, Listing L, Textbook T '
					  'WHERE S.seller_id = L.seller_id AND L.ISBN = T.ISBN '
					   "AND L.listing_state = 'Public' "
					  'and u.username = S.username '
					  'and T.title = %s AND L.price > %s AND L.Price < %s')
					  
		rs.execute(SearchSell, (textbookTitle, lowPrice, highPrice))
		
		print
		for (a,b,c,d,e,f) in rs:
			result = 'Listing ID: {}, Seller: {}, {}, ${}, Condition: {}, Date Posted: {}'.format(a,b,c,d,e,f)
			print(result)
		print
	elif userChoice == 5:
		searchListings(con, rs, buyerID)
	elif userChoice == 6:
		lowestPrice = (' SELECT L.listing_id, S.username, T.title, L.price, L.book_condition,  L.date_listed'
			       ' FROM Seller S JOIN Listing L using(seller_id), Textbook T '
			       ' WHERE L.ISBN = T.ISBN and T.title = %s and L.listing_state = "Public" '
			       '       AND  L.price = (SELECT min(Y.price) '
							' FROM Seller X JOIN Listing Y using(seller_id), Textbook Z '
							' WHERE Y.ISBN = Z.ISBN and Z.title = %s and Y.listing_state = "Public")')
		rs.execute(lowestPrice,(textbookTitle,textbookTitle))
		print
		for(a,b,c,d,e,f) in rs:
			result = 'Listing ID: {}, Seller: {}, {}, ${}, Condition: {}, Date Posted: {}'.format(a,b,c,d,e,f)
			print(result)

	elif userChoice == 7:
		exit()
	else:
		print("Please enter a valid choice (1-7)")
		searchListingsMenu(con, rs, textbookTitle, buyerID)

	searchListingsMenu(con,rs,textbookTitle, buyerID)
	
def requestTextbook(con, rs, buyerID, textbookTitle):
	print
        listingID = raw_input("Enter listing number you wish to request: ")
	date = datetime.datetime.now().strftime("%y-%m-%d")
	
	#findListing = '''SELECT l.listing_id FROM Listing l'''
	#rs.execute(findListing)
	#isFound = False
	#for(a) in rs:
	#    list_id = '{}'.format(a)
    #        if list_id == listingID:
    #            isFound = True
	#if not isFound:
	#	print("\nListing does not exist")
	#	requestTextbook(con,rs,buyerID, textbookTitle)
	
	findListing = '''SELECT l.listing_id, l.seller_id FROM Listing l
						WHERE l.listing_id = %s'''

        rs.execute(findListing, (listingID,))
	
	row = rs.fetchone()
	if row is not None:
		list_id = row[0]
		sell_id = row[1]
	else:
		print("\n\tListing does not exist")
		requestTextbook(con, rs, buyerID, textbookTitle)
		
	check = '''SELECT r.listing_id, r.buyer_id
				FROM Request r'''
	rs.execute(check)
	
	isFound = False
	
	for (a,b) in rs:
		list = '{}'.format(a)
		buy = '{}'.format(b)
		if buyerID == buy and list == listingID:
			isFound = True
	if not isFound:
	    insertReq = 'INSERT INTO Request( date_requested, request_state, listing_id, seller_id, buyer_id) VALUES( %s, %s, %s, %s, %s)'
	    rs.execute(insertReq, ( date,'Pending',list_id,sell_id, buyerID))
	    con.commit()	
	
	    print("Book has been requested, returning to main menu")
	else:
		print("You have already made a request for this listing")
	buyerMenuDisplay(con, rs, buyerID)


#-------------------------------------------------------------------#
#Below is seller options, above is buyer options
#-------------------------------------------------------------------#

#this function displays the menu for the seller's options
def sellerMenuDisplay(con, rs, sellerID):
    print
    print("Your Menu:")
    print("	1. See my textbooks on sale")
    print("	2. Hide a textbook listing")
    print("	3. Add a textbook listing")
    print("	4. See pending requests for textbooks")
    print("	5. Exit")
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
    print
    print("These are your textbooks on sale: ")
    query = '''SELECT t.title as title, l.date_listed as date_listed, l.price as price, l.book_condition as book_condition
               FROM Listing l JOIN Seller s USING (seller_id) JOIN Textbook t USING (ISBN)
               WHERE seller_id = %s 
			   AND l.listing_state = 'Public';
            '''
    rs.execute(query, (sellerID,))
    
    for(title, date_listed, price, book_condition) in rs:
        print 'Title: {}, Date Listed: {}, ${}, Condition: {}'.format(title, date_listed, price, book_condition)

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
        print 'Listing ID: {}, ISBN:{}, CRN: {}, Date Listed: {}, ${}, Condition{}'.format(listing_id, ISBN, CRN, date_listed, price, book_condition)

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
    price = input("Please enter the price of the textbook: $")
	
    print("Here are the options for the book condition: ")
    print("1. Poor")
    print("2. Fair")
    print("3. Good")
    print("4. Very Good")
    print("5. Like New")
	
    date_listed = datetime.datetime.now().strftime("%y-%m-%d")
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
    print("Pending Textbook Requests")
    query = '''SELECT r.request_id, r.date_requested, r.request_state, b.username
               FROM Request r JOIN Buyer b USING (buyer_id) 
               WHERE r.seller_id = %s
		AND r.request_state = 'Pending'	'''
    rs.execute(query,(sellerID,))
    for(rid, date_requested, request_state, buyer_name) in rs:
        print 'Request ID: {}, Date Requested: {}, {} buyer: {}'.format(rid, date_requested, request_state, buyer_name)
		
	print
	print("1. Approve a Request ")
        print("2. Decline a Request")
	print("3. Return to menu")
	userInput = raw_input("Enter choice: ")
	
	if userInput == '1' or userInput == '1 ':
	    requestID = input("Enter request ID to approve: ")
            update = '''UPDATE Request
        	            SET request_state = 'Approved'
				WHERE request_id = %s'''
            rs.execute(update, (requestID,))
	    con.commit();
            update2 = '''UPDATE Listing
                           SET listing_state = 'Hidden'
                          WHERE listing_id = (SELECT r.listing_id
                                               FROM  Request r
                                              WHERE r.request_id = %s)'''
            rs.execute(update, (requestID,))
            con.commit();
	    print("Your email address has been given to the buyer")
	elif userInput == '2' or userInput == '2 ':
            requestID = input("Enter request ID to decline: ")
            update = '''UPDATE Request
                          SET request_state = 'Declined'
                         WHERE request_id = %s'''
            rs.execute(update, (requestID,))
            con.commit();
            print("This request has been declined")	
	elif userInput == '3' or userInput == '3 ':
            sellerMenuDisplay(con, rs, sellerID)
	else:
		print("Error")
                seeTextbookRequests(con, rs, sellerID)


if __name__ == '__main__':
	main()	
