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
INSERT INTO sayings
VALUES ("Hello, world!");
INSERT INTO sayings
VALUES ("Hello, bagels!");
INSERT INTO sayings
VALUES ("Hello, butter!");
INSERT INTO sayings
VALUES ("Hello, system!");
