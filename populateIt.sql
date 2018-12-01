DROP TABLE IF EXISTS Request;
DROP TABLE IF EXISTS Listing;
DROP TABLE IF EXISTS CourseTextbook;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Textbook;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Buyer;

CREATE TABLE Buyer(
	buyer_id		INT NOT NULL,
	name			VARCHAR(25),
	email			VARCHAR(40),
	PRIMARY KEY(buyer_id)
) engine = InnoDB;

CREATE TABLE Seller(
	seller_id 		INT NOT NULL,
	name			VARCHAR(20),
	email			VARCHAR(40),
	PRIMARY KEY(seller_id)
) engine = InnoDB;

CREATE TABLE Textbook(
	textbook_id  	INT NOT NULL,
	ISBN		 	VARCHAR(13),
	title		 	VARCHAR(40),
	author		 	VARCHAR(30),
	edition		 	INT,
	publisher	 	VARCHAR(40),
	year_published 	YEAR,
	PRIMARY KEY(textbook_id)
	) engine = InnoDB;

CREATE TABLE Course(
	CRN				INT(5) NOT NULL,
	department		VARCHAR(4),
	course_number	INT(4) NOT NULL,
	course_section	INT(2) NOT NULL,
	instructor		VARCHAR(40),
	term			ENUM('Fall', 'Spring', 'Summer'),
	course_year		YEAR,
	PRIMARY KEY(CRN)
	) engine = InnoDB;

CREATE TABLE CourseTextbook(
	textbook_id		INT NOT NULL,
	CRN				INT NOT NULL,
	PRIMARY KEY (textbook_id, CRN),
	FOREIGN KEY (textbook_id) REFERENCES Textbook(textbook_id),
	FOREIGN KEY (CRN) REFERENCES Course(CRN)
	) engine = InnoDB;

CREATE TABLE Listing(
	listing_id	    INT NOT NULL,
	seller_id		INT NOT NULL,
	textbook_id		INT NOT NULL,
	CRN				INT NOT NULL,
	date_listed	    DATE,              -- YYYY-MM-DD
	price		    INT NOT NULL,
	book_condition	ENUM('Poor', 'Fair', 'Good', 'Very Good', 'Like New'),
	listing_state 	ENUM('Public', 'Hidden'),
	PRIMARY KEY (listing_id),
	FOREIGN KEY (textbook_id) REFERENCES Textbook(textbook_id),
	FOREIGN KEY (CRN) REFERENCES Course(CRN),
	FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
	) engine = InnoDB;

CREATE TABLE Request(
	request_id	    INT NOT NULL,
	date_requested  DATE,             -- YYYY-MM-DD
	request_state	ENUM('Pending', 'Approved', 'Declined'),
	listing_id	    INT NOT NULL,
	seller_id		INT NOT NULL,
	buyer_id		INT NOT NULL,
	PRIMARY KEY (request_id),
	FOREIGN KEY (listing_id) REFERENCES Listing(listing_id),
	FOREIGN KEY (seller_id) REFERENCES Seller(seller_id),
	FOREIGN KEY (buyer_id)	REFERENCES Buyer(buyer_id)
	) engine=InnoDB;


INSERT INTO Buyer VALUES
	(1,'John James','jjames@zagmail.gonzaga.edu'),
	(2,'Paul Yurmp', 'pyurmp@zagmail.gonzaga.edu'),
	(3,'Joe Evans','jevans3@zagmail.gonzaga.edu'),
	(4,'Ellen Grey','egrey@zagmail.gonzaga.edu'),
	(5,'Collin Fisher', 'cfisher2@zagmail.gonzaga.edu');

INSERT INTO Seller VALUES
	(1,'Michelle Stevenson','mstevenson@zagmail.gonzaga.edu'),
	(2,'Kyle Kip','kkip@zagmail.gonzaga.edu'),
	(3,'Tyler Drake', 'tdrake@zagmail.gonzaga.edu'),
	(4,'Stacy Smith', 'ssmith7@zagmail.gonzaga.edu'),
	(5,'Scott Howlett','showlett@zagmail.gonzaga.edu');

INSERT INTO Textbook VALUES
	(1, '9781234567891', 'Computer Hardware', 'Greg Computer', 2, 'Jacobs Publishing Inc.', 2016),
	(2, '9781469894201', 'Basics of Nursing', 'John Patrick', 11, 'Dolphin Press', 2004),
	(3, '9780471121206', 'Chemisty: Concepts and Problems', 'Richard Post', 2, 'Wiley', 1996),
	(4, '9781118063330', 'Operating System Concepts', 'Abraham Silvershatz', 9, 'Wiley', 2012),
	(5, '9780073523323', 'Database System Concepts', 'Abraham Silvershatz', 6, 'McGraw-Hill Education', 2010);

INSERT INTO Course VALUES
	(11485, 'CPSC', '321', '01', 'Shawn Bowers', 'Fall', 2018),
	(11014, 'CPSC', '346', '02', 'Paul DePalma', 'Fall', 2018),
	(21402, 'CHEM', '104', '07', 'Bill Nye', 'Spring', 2019),
	(12345, 'COMM', '425', '03', 'Allison Davis', 'Spring', 2019),
	(13562, 'NURS', '372', '01', 'Erica Fisher', 'Spring', 2019);