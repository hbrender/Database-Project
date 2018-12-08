DROP TABLE IF EXISTS Request;
DROP TABLE IF EXISTS Listing;
DROP TABLE IF EXISTS CourseTextbook;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Textbook;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Buyer;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users(
	username		VARCHAR(20) NOT NULL,
	password		VARCHAR(10) NOT NULL,
	name			VARCHAR(25),
	PRIMARY KEY (username)
) engine = InnoDB;

CREATE TABLE Buyer(
	buyer_id		INT NOT NULL AUTO_INCREMENT,
	username		VARCHAR(10) NOT NULL,
	PRIMARY KEY(buyer_id, username),
	FOREIGN KEY (username) REFERENCES Users(username)
) engine = InnoDB;

CREATE TABLE Seller(
	seller_id 		INT NOT NULL AUTO_INCREMENT,
	username		VARCHAR(10) NOT NULL,
	PRIMARY KEY(seller_id, username),
	FOREIGN KEY (username) REFERENCES Users(username)
) engine = InnoDB;

CREATE TABLE Textbook(
	ISBN		 	VARCHAR(13) NOT NULL,
	title		 	VARCHAR(40),
	author		 	VARCHAR(30),
	edition		 	INT,
	publisher	 	VARCHAR(40),
	year_published 	YEAR,
	price			DECIMAL(5,2),
	PRIMARY KEY(ISBN)
) engine = InnoDB;

CREATE TABLE Course(
	CRN				INT(5) NOT NULL,
	department		VARCHAR(4),
	course_number	VARCHAR(4) NOT NULL,
	course_section	VARCHAR(2) NOT NULL,
	instructor		VARCHAR(40),
	term			ENUM('Fall', 'Spring', 'Summer'),
	course_year		YEAR,
	PRIMARY KEY(CRN)
) engine = InnoDB;

CREATE TABLE CourseTextbook(
	ISBN		VARCHAR(13) NOT NULL,
	CRN			INT(5) NOT NULL,
	PRIMARY KEY (ISBN, CRN),
	FOREIGN KEY (ISBN) REFERENCES Textbook(ISBN),
	FOREIGN KEY (CRN) REFERENCES Course(CRN)
) engine = InnoDB;

CREATE TABLE Listing(
	listing_id	    INT NOT NULL AUTO_INCREMENT,
	seller_id		INT NOT NULL,
	ISBN			VARCHAR(13) NOT NULL,
	CRN				INT NOT NULL,
	date_listed	    DATE,              -- YYYY-MM-DD
	price		    INT NOT NULL,
	book_condition	ENUM('Poor', 'Fair', 'Good', 'Very Good', 'Like New'),
	listing_state 	ENUM('Public', 'Hidden'),
	PRIMARY KEY (listing_id),
	FOREIGN KEY (ISBN) REFERENCES Textbook(ISBN),
	FOREIGN KEY (CRN) REFERENCES Course(CRN),
	FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
) engine = InnoDB;

ALTER TABLE Listing AUTO_INCREMENT = 1;

CREATE TABLE Request(
	request_id	    INT NOT NULL AUTO_INCREMENT,
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

ALTER TABLE Request AUTO_INCREMENT = 1;


INSERT INTO Users VALUES
	('jjames', 'password1', 'John James'),
	('pyurmp', 'password2', 'Paul Yurmp'),
	('jevans3', 'password3', 'Joe Evans'),
	('egrey', 'password4', 'Ellen Grey'),
	('cfisher2', 'password5', 'Collin Fisher'),
	('mstevenson', 'password6', 'Michelle Stevenson'),
	('kkip', 'password7', 'Kyle Kip'),
	('tdrake', 'password8', 'Tyler Drake'),
	('ssmith7', 'password9', 'Stacy Smith'),
	('showlett', 'password10', 'Scott Howlett');

INSERT INTO Buyer (username) VALUES
	('jjames'),
	('pyurmp'),
	('jevans3'),
	('egrey'),
	('cfisher2');

INSERT INTO Seller (username) VALUES
	('mstevenson'),
	('kkip'),
	('tdrake'),
	('ssmith7'),
	('showlett');

INSERT INTO Textbook VALUES
	('9781234567891', 'Computer Hardware', 'Greg Computer', 2, 'Jacobs Publishing Inc.', 2016, 157.00),
	('9781469894201', 'Basics of Nursing', 'John Patrick', 11, 'Dolphin Press', 2004, 89.99),
	('9780471121206', 'Chemisty: Concepts and Problems', 'Richard Post', 2, 'Wiley', 1996, 210.00),
	('9781118063330', 'Operating System Concepts', 'Abraham Silvershatz', 9, 'Wiley', 2012, 74.99),
	('9780073523323', 'Database System Concepts', 'Abraham Silvershatz', 6, 'McGraw-Hill Education', 2010, 40.00);

INSERT INTO Course VALUES
	(11485, 'CPSC', '321', '01', 'Shawn Bowers', 'Fall', 2018),
	(11014, 'CPSC', '346', '02', 'Paul DePalma', 'Fall', 2018),
	(21402, 'CHEM', '104', '07', 'Bill Nye', 'Spring', 2019),
	(12345, 'COMM', '425', '03', 'Allison Davis', 'Spring', 2019),
	(13562, 'NURS', '372', '01', 'Erica Fisher', 'Spring', 2019);
	
INSERT INTO CourseTextbook VALUES
	('9781234567891', 11014),
	('9781118063330', 11014),
	('9780471121206', 21402),
	('9780073523323', 11485),
	('9781469894201', 13562);

INSERT INTO Listing VALUES 
	(1, 5, 9781234567891, 11014, '2018-05-09', 50, 'Good', 'Public'),
	(2, 3, 9781234567891, 11014, '2018-05-27', 75, 'Very Good', 'Public'),
 	(3, 4, 9781234567891, 11014, '2018-04-18', 30, 'Fair', 'Hidden');
	
-- INSERT INTO Request VALUES
	-- (1, '2018-12-07', 'Pending', 1, 

/*	
SELECT ct.CRN, c.department, c.course_number, c.course_section, c.instructor, t.title, t.ISBN
FROM CourseTextbook ct, Course c, Textbook t
WHERE c.CRN = 11014
AND ct.CRN = c.CRN
AND t.ISBN = ct.ISBN;
SELECT ct.CRN, c.department, c.course_number, c.course_section, c.instructor, t.title, t.ISBN
FROM CourseTextbook ct, Course c, Textbook t
WHERE c.CRN = NULL
AND c.department = 'CPSC'
AND ct.CRN = c.CRN
AND t.ISBN = ct.ISBN;
*/