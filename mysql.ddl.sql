-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fcc_comments
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.14.04.1

--
-- Current Database: `fcc_comments`
--

CREATE DATABASE `fcc_comments`;

USE `fcc_comments`;

--
-- Table structure for table `comments`
--
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` bigint(20) NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `date_submitted` datetime DEFAULT NULL,
  `link` varchar(256) DEFAULT NULL,
  `proceeding` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `city` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE USER 'fccwebuser'@'localhost' IDENTIFIED BY 'changeit';
GRANT SELECT, INSERT ON 'fcc_comments'.* TO 'fccwebuser2'@'localhost';
FLUSH PRIVILEGES;

-- Dump completed on 2014-06-06 18:55:42
