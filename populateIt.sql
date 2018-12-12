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
	('showlett', 'password10', 'Scott Howlett'),
	('hbrender', '12', 'Hanna Brender');

INSERT INTO Buyer (username) VALUES
	('jjames'),
	('pyurmp'),
	('jevans3'),
	('egrey'),
	('cfisher2'),
	('hbrender');

INSERT INTO Seller (username) VALUES
	('mstevenson'),
	('kkip'),
	('tdrake'),
	('ssmith7'),
	('showlett'),
	('hbrender');

INSERT INTO Textbook VALUES
	('9781234567891', 'Computer Hardware', 'Greg Computer', 2, 'Jacobs Publishing Inc.', 2016, 157.00),
	('9781469894201', 'Basics of Nursing', 'John Patrick', 11, 'Dolphin Press', 2004, 89.99),
	('9780471121206', 'Chemisty: Concepts and Problems', 'Richard Post', 2, 'Wiley', 1996, 210.00),
	('9781118063330', 'Operating System Concepts', 'Abraham Silvershatz', 9, 'Wiley', 2012, 74.99),
	('9780073523323', 'Database System Concepts', 'Abraham Silvershatz', 6, 'McGraw-Hill Education', 2010, 40.00),
	('1234567890123', 'Jazz in 1960','Irst Hemmer', 1, 'Hackett Book', 2017,140.00 ),
	('2345678901234', 'Education for Children','Spencer Flep',2 , 'Harvard Press',2012 ,50.00 ),
	('3456789012345', 'The human Brain and Love','Isaac Vance',1 , 'Harlequin', 2010,70.00 ),
	('4567890123456', 'Society of Ancient Israel','Isaiah Heyt',4 , 'Hachette Books', 2009,90.00 ),
	('5678901234567', 'Inside of Computers','Colin Cumberbatch',1 , 'Highwire',2001 ,100.00 ),
	('6789012345678', 'Mechanics of Materials','Jason Match',2 , 'Hackett Book',2004 ,210.00 ),
	('7890123456789', 'For Whom the Bell Tolls','Hyf Shweinstizer',4 , 'HarperCollins',2010 ,40.00),
        ('9781891136375','Rhetoric in Civic Life','Palczewski',2,'Strata Publishing, Inc.',2012,15.00),
        ('9780321927040', 'Human Anatomy & Physiology', 'Elaine Marieb',10,'Pearson Education',2015,67.99),
        ('9780134093413','Campbell Biology','Lisa Urry',11,'Pearson Education',2016,171.49);

INSERT INTO Course VALUES
	(11485, 'CPSC', '321', '01', 'Shawn Bowers', 'Fall', 2018),
	(11014, 'CPSC', '346', '02', 'Paul DePalma', 'Fall', 2018),
	(21402, 'CHEM', '104', '07', 'Bill Nye', 'Spring', 2019),
	(12345, 'COMM', '425', '03', 'Allison Davis', 'Spring', 2019),
	(13562, 'NURS', '372', '01', 'Erica Fisher', 'Spring', 2019),
	(32453, 'MUSC', '101', '01', 'Jimmy John', 'Fall', 2018),
	(21875, 'EDUC', '123', '01', 'Shell Siil', 'Fall', 2018),
	(94836, 'PYSC', '234', '02', 'Adam Fitzer', 'Fall', 2018),
	(35271, 'SOCI', '432', '07', 'Niel Grom', 'Spring', 2019),
	(96382, 'CPEN', '121', '03', 'Al Adams', 'Spring', 2019),
	(45673, 'MECH', '163', '01', 'Seth OReilly', 'Spring', 2019),
	(43561, 'ENGL', '234', '01', 'Jeff Master', 'Fall', 2018),
        (10939, 'COMM', '100', '01', 'Tracy Struble','Fall',2018);

	
INSERT INTO CourseTextbook VALUES
	('9781234567891', 11014),
	('9781118063330', 11014),
	('9780471121206', 21402),
	('9780073523323', 11485),
	('9781469894201', 13562),
	('1234567890123', 32453),
	('2345678901234', 21875),
	('3456789012345', 94836),
	('4567890123456', 35271),
	('5678901234567', 96382),
	('6789012345678', 45673),
	('7890123456789', 43561),
        ('9781891136375', 10939);

INSERT INTO Listing VALUES 
	(1, 5, '9781234567891', 11014, '2018-05-09', 50, 'Good', 'Public'),
	(2, 3, '9781234567891', 11014, '2018-05-27', 75, 'Very Good', 'Public'),
 	(3, 4, '9781234567891', 11014, '2018-04-18', 30, 'Fair', 'Hidden'),
	(11, 2, '9781234567891', 11014, '2018-12-11', 100, 'Like New', 'Public'),
	(12, 1, '9781234567891', 11014, '2018-12-10', 19, 'Poor', 'Public'),
	(4, 3, '1234567890123', 32453, '2018-04-19', 40, 'Good', 'Public'),
	(5, 2, '2345678901234', 21875, '2018-01-01', 50, 'Very Good', 'Public'),
	(6, 1, '3456789012345', 94836, '2018-05-07', 70, 'Fair', 'Public'),
	(7, 3, '4567890123456', 35271, '2018-12-08', 50, 'Fair', 'Public'),
	(8, 2, '5678901234567', 96382, '2018-11-12', 70, 'Very Good', 'Public'),
	(9, 5, '6789012345678', 45673, '2018-10-08', 40, 'Good', 'Public'),
	(10, 2, '7890123456789', 43561, '2018-9-27', 70, 'Very Good', 'Public'),
	(14, 6, '4567890123456', 35271, '2018-12-11', 65, 'Good', 'Public'),
	(15, 6, '9781469894201', 13562, '2018-11-25', 45, 'Fair', 'Public'),
	(13, 6, '9780073523323', 11485, '2018-05-23', 100, 'Like New', 'Public');

INSERT INTO Request VALUES
	(1, '2018-12-08', 'Pending', 1, 5, 6),
	(2, '2018-12-10', 'Pending', 2, 3, 6),
	(3, '2018-10-10', 'Approved', 11, 3, 6), 
	(4, '2018-12-10', 'Declined', 5, 2, 6),
	(5, '2018-12-11', 'Pending', 14, 6, 2),
	(6, '2018-12-11', 'Pending', 13, 6, 1),
        (7, '2019-01-02', 'Pending', 4, 3,4),
        (8, '2018-12-06', 'Pending', 3, 4, 4),
        (9, '2018-12-06', 'Pending', 1, 5, 5),
        (10,'2018-12-07', 'Pending', 1, 5, 1),
        (11,'2018-12-08', 'Pending', 1, 5, 2), 
        (12, '2018-12-08', 'Pending',1, 5, 3); 
