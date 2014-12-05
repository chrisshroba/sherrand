CREATE DATABASE IF NOT EXISTS test;
USE test;
CREATE TABLE IF NOT EXISTS sayings
(
    saying VARCHAR(30)
);
CREATE TABLE IF NOT EXISTS Requests
(
  Id MEDIUMINT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(140),
  User MEDIUMINT NOT NULL,
  StartDateTime DATETIME NOT NULL,
  EndDateTime DATETIME NOT NULL,
  OriginName VARCHAR(140),
  OriginLat FLOAT(10, 6) NOT NULL,
  OriginLng FLOAT(10, 6) NOT NULL,
  DestinationName VARCHAR(140),
  DestinationLat FLOAT(10, 6) NOT NULL,
  DestinationLng FLOAT(10, 6) NOT NULL,
  PRIMARY KEY (Id)
);

CREATE TABLE IF NOT EXISTS Offers
(
  Id MEDIUMINT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(140),
  User MEDIUMINT NOT NULL,
  MaxSeats INT NOT NULL,
  OpenSeats INT NOT NULL,
  StartDateTime DATETIME NOT NULL,
  EndDateTime DATETIME NOT NULL,
  OriginName VARCHAR(140),
  OriginLat FLOAT(10, 6) NOT NULL,
  OriginLng FLOAT(10, 6) NOT NULL,
  DestinationName VARCHAR(140),
  DestinationLat FLOAT(10, 6) NOT NULL,
  DestinationLng FLOAT(10, 6) NOT NULL,
  PRIMARY KEY (Id)
);

CREATE TABLE IF NOT EXISTS Users 
(
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  username varchar(30) DEFAULT NULL,
  password varchar(160) DEFAULT NULL,
  first_name varchar(60) DEFAULT NULL,
  last_name varchar(60) DEFAULT NULL,
  phone varchar(16) DEFAULT NULL,
  email varchar(40) DEFAULT NULL,
  score int(11) DEFAULT NULL,
  photo varchar(40) DEFAULT NULL,
  driver_rating double DEFAULT 0,
  passenger_rating double DEFAULT 0,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Rides 
(
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  offer_id int NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Passengers 
(
  user_id int NOT NULL,
  ride_id int NOT NULL,
  PRIMARY KEY (user_id, ride_id)
);

CREATE TABLE IF NOT EXISTS Notifications
(
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  user_id MEDIUMINT NOT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  message VARCHAR(140) NOT NULL,
  link VARCHAR(140) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO sayings
VALUES ("Hello, world!");
INSERT INTO sayings
VALUES ("Hello, bagels!");
INSERT INTO sayings
VALUES ("Hello, butter!");
INSERT INTO sayings
VALUES ("Hello, system!");

INSERT INTO Users (first_name, last_name, username, password, phone, email)
VALUES ("asdf", "asdf", "asdf",PASSWORD("asdf"), "0000000000", "asdf@gmail.com")
