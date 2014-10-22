CREATE DATABASE IF NOT EXISTS test;
USE test;
CREATE TABLE IF NOT EXISTS sayings
(
    saying VARCHAR(30)
);
INSERT INTO sayings
VALUES ("Hello, world!");
INSERT INTO sayings
VALUES ("Hello, bagels!");
INSERT INTO sayings
VALUES ("Hello, butter!");
INSERT INTO sayings
VALUES ("Hello, system!");


CREATE TABLE Users (
      username varchar(30) DEFAULT NULL,
      pass varchar(160) DEFAULT NULL,
      user_id int(11) NOT NULL AUTO_INCREMENT,
      full_name varchar(60) DEFAULT NULL,
      phone varchar(16) DEFAULT NULL,
      email varchar(40) DEFAULT NULL,
      score int(11) DEFAULT NULL,
      photo varchar(40) DEFAULT NULL,
      driver_rating double DEFAULT NULL,
      passenger_rating double DEFAULT NULL,
      PRIMARY KEY (user_id)
);
