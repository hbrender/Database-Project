DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Textbook;
DROP TABLE IF EXISTS Listing;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Request;
DROP TABLE IF EXISTS Buyer;

CREATE TABLE Buyer(
	buyer_id	int not null,
	name		varchar(25),
	email		varchar(30),
	PRIMARY KEY(buyer_id)
) engine = InnoDB;

CREATE TABLE Seller(
	seller_id 	int not null,
	name		varchar(20),
	email		varchar(30),
	PRIMARY KEY(seller_id)
) engine = InnoDB;

CREATE TABLE Textbook(
	textbook_id 	int not null,
	ISBN		int,
	title		varchar(40),
	author		varchar(30),
	edition		int,
	publisher	varchar(40),
	date_published	varchar(40),
	PRIMARY KEY(textbook_id)
	) engine = InnoDB;

CREATE TABLE Course(
	CRN		int not null,
	department	varchar(20),
	course_number	int,
	course_section	int,
	instructor	varchar(20),
	term		varchar(20),
	year		int,
	PRIMARY KEY(CRN)
	) engine = InnoDB;

CREATE TABLE Listing(
	listing_id	int not null,
	date_listed	varchar(20),
	price		int not null,
	conditionOfBook	varchar(10),
	PRIMARY KEY(listing_id)
	) engine = InnoDB;

CREATE TABLE Request(
	request_id	 int not null,
	date_requested 	 varchar(10),
	request_state	 varchar(10),
	listing_id	 int not null,
	textbook_id	 int not null,
	PRIMARY KEY (request_id)
	) engine=InnoDB;


INSERT INTO Buyer VALUES
	(1,'John James','JJames@zagmail.gonzaga.edu'),
	(2,'Paul Yurmp', 'PYurmp@zagmail.gonzaga.edu');

INSERT INTO Seller VALUES
	(1,'Michelle Stevenson', 'MStevenson@zagmail.gonzaga.edu'),
	(2,'Kyle Kip', 'kkip@zagmail.gonzaga.edu');

INSERT INTO Textbook VALUES
	(1, 1234, 'Biology 101', 'Author1', 2, 'jacobs publishing inc', '11/28/2018');

INSERT INTO Course VALUES
	(20280, 'Biology', 23, 1, 'Mr. bioman', 'Spring', 2019);
	
