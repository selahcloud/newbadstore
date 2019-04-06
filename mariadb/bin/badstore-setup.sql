-- MySQL dump 10.11
--
-- Host: localhost    Database: badstoredb
-- ------------------------------------------------------
-- Server version	5.0.96-0ubuntu3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acctdb`
--

DROP TABLE IF EXISTS `acctdb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acctdb` (
  `invnum` varchar(20) default NULL,
  `amount` float(8,2) default NULL,
  `status` varchar(10) default NULL,
  `paidon` date default NULL,
  `bankinfo` varchar(20) default NULL,
  `rma` char(1) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acctdb`
--

LOCK TABLES `acctdb` WRITE;
/*!40000 ALTER TABLE `acctdb` DISABLE KEYS */;
INSERT INTO `acctdb` VALUES ('MS-45921',4976.48,'Paid','2010-05-10','33011:38349873766','0'),('MS-45876',983.93,'Submitted','2010-05-10','33011:38349873766','1'),('MS-45873',34897.21,'Received','2010-05-09','78011:38334587297','0');
/*!40000 ALTER TABLE `acctdb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemdb`
--

DROP TABLE IF EXISTS `itemdb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `itemdb` (
  `itemnum` int(11) default NULL,
  `sdesc` varchar(20) default NULL,
  `ldesc` varchar(40) default NULL,
  `qty` int(11) default NULL,
  `cost` float(8,2) default NULL,
  `price` float(8,2) default NULL,
  `isnew` varchar(1) default NULL,
  `catg` varchar(20) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemdb`
--

LOCK TABLES `itemdb` WRITE;
/*!40000 ALTER TABLE `itemdb` DISABLE KEYS */;
INSERT INTO `itemdb` VALUES (1000,'Snake Oil','Useless but expensive',5,4.35,11.50,'Y','Personal'),(1001,'Crystal Ball','The finest Austrian crystal for complete',2,13.95,49.95,'N','Magic'),(1003,'Magic Rabbit','Cute white bunny',27,3.50,12.50,'Y','Magic'),(1004,'Security Appliance','Everybody needs one',3,400.00,3999.00,'N','Home'),(1005,'Perfect Code','The rarest magic of all',1,5.00,5000.00,'Y','Office'),(1002,'Magic Hat','The classic magicians hat',7,18.45,60.00,'N','Magic'),(1007,'Bag o Fud','For those who believe anything',9,2.50,200.00,'N','Magic'),(1008,'ROI Calculator','Accurate Return on Investment',99,2.30,22.95,'Y','Gadget'),(1009,'Planning Template','Business Planning Tool',2,6.70,24.95,'Y','Office'),(1010,'Security 911','Technical Support Agreement',1,99.00,9999.00,'N','Personal'),(1011,'Money','There\'s never enough',1,3.00,90.00,'Y','Commercial'),(1012,'Endless Cup','Perfect for late nights',74,4.56,23.98,'Y','Home'),(1013,'Invisibility Cloak','For when you just want to hide',1,0.00,8995.00,'N','Magic'),(1014,'Disappearing Ink','Makes perfect signatures',43,8.96,30.95,'Y','Magic'),(1015,'Apple ipad','Tablet computer',20,15.09,599.35,'Y','Gadget'),(1016,'Shoes','Nike Shoes',3,8.96,350.25,'Y','Sports'),(1017,'This is it','Michael Jackson CD',43,8.96,20.95,'Y','Music'),(1018,'Xperia','Sony Xperia Mobile',3,45.96,700.24,'Y','Gadget');
/*!40000 ALTER TABLE `itemdb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderdb`
--

DROP TABLE IF EXISTS `orderdb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderdb` (
  `sessid` int(11) default NULL,
  `orderdate` date default NULL,
  `ordertime` time default NULL,
  `ordercost` varchar(10) default NULL,
  `orderitems` int(11) default NULL,
  `itemlist` varchar(50) default NULL,
  `accountid` varchar(30) default NULL,
  `ipaddr` varchar(20) default NULL,
  `cartpaid` varchar(1) default NULL,
  `ccard` varchar(16) default NULL,
  `expdate` varchar(4) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderdb`
--

LOCK TABLES `orderdb` WRITE;
/*!40000 ALTER TABLE `orderdb` DISABLE KEYS */;
INSERT INTO `orderdb` VALUES (1078228766,'2010-05-10','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.50','Y','4111111111111111','0705'),(1078228767,'2010-05-10','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.150','Y','5500000000000004','0905'),(1078229834,'2010-05-09','12:29:24','$22.95',1,'1008','joe@supplier.com','10.10.10.50','Y','340000000000009','1008'),(1078232948,'2010-05-09','10:24:23','$144.93',3,'1011,1012,1014','mary@spender.com','192.168.10.70','Y','30000000000004','0506'),(1078232048,'2010-05-09','12:29:25','$137.90',3,'1008,1009,1011','sue@spender.com','10.10.10.350','Y','601100000004','1006'),(1078228766,'2010-05-10','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.50','Y','4111111111111111','0705'),(1078228767,'2010-05-08','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.150','Y','5500000000000004','0905'),(1078229834,'2010-05-08','04:20:21','$22.95',1,'1008','joe@supplier.com','10.10.10.50','Y','340000000000009','1008'),(1078232048,'2010-05-08','09:55:17','$137.90',3,'1008,1009,1011','mary@spender.com','192.168.10.70','Y','30000000000004','0506'),(1078232048,'2010-05-08','12:29:25','$137.90',3,'1008,1009,1011','sue@spender.com','10.10.10.350','Y','6011000000000004','1006'),(1078228766,'2010-05-07','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.50','Y','4111111111111111','0705'),(1078228767,'2010-05-07','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.150','Y','5500000000000004','0905'),(1078229834,'2010-05-07','12:29:25','$22.95',1,'1008','joe@supplier.com','10.10.10.50','Y','340000000000009','1008'),(1078232048,'2010-05-07','12:29:25','$137.90',3,'1008,1009,1011','mary@spender.com','192.168.10.70','Y','30000000000004','0506'),(1078232048,'2010-05-06','09:23:23','$137.90',3,'1008,1009,1011','sue@spender.com','10.10.10.350','Y','6011000000000004','1006'),(1078228766,'2010-05-04','05:27:17','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.50','Y','4111111111111111','0705'),(1078228767,'2010-05-03','12:29:25','$46.95',3,'1000,1003,1008','joe@supplier.com','10.10.10.150','Y','5500000000000004','0905'),(1078229834,'2010-04-27','10:25:16','$22.95',1,'1008','joe@supplier.com','10.10.10.50','Y','340000000000009','1008'),(1078232048,'2010-04-21','12:29:25','$137.90',3,'1008,1009,1011','mary@spender.com','192.168.10.70','Y','30000000000004','0506'),(1078232388,'2010-04-21','12:29:25','$1137.90',3,'1008,1009,1011','sue@spender.com','10.10.10.350','Y','6011000000000004','1006'),(1078233380,'2010-04-05','12:29:25','$360.00',1,'1002','fred@newuser.com','172.22.15.47','Y','201400000000009','0705'),(1273551639,'2010-05-11','04:21:13','$20.95',1,'1017','abhi@abhi.com','192.168.128.43','Y','4111111111111111','1212'),(1273551912,'2010-05-11','04:25:31','$12.50',1,'1003','rishi@rish.com','192.168.128.43','Y','5000000000000004','1010'),(1273551943,'2010-05-11','04:26:06','$22.95',1,'1008','rishi@rish.com','192.168.128.43','Y','5000000000000004','2121'),(1273551972,'2010-05-11','04:27:54','$12.50',1,'1003','rishi@rish.com','192.168.128.43','Y','5000000000000004','1010'),(1273552082,'2010-05-11','04:28:24','$599.35',1,'1015','rishi@rish.com','192.168.128.43','Y','4111111111111111','1212'),(1276757590,'2010-06-17','06:53:30','$5012.50',2,'1003,1005','abhi@abhi.com','192.168.128.43','Y','4111111111111111','1212'),(1276757623,'2010-06-17','06:54:13','$12.50',1,'1003','abhi@abhi.com','192.168.128.43','Y','5000000000000004','1111'),(1276757667,'2010-06-17','06:54:39','$5000.00',1,'1005','abhi@abhi.com','192.168.128.43','Y','5000000000000004','1111'),(1354159860,'2012-11-29','03:31:10','$11.50',1,'1000','test@x.com','10.11.18.16','Y','','');
/*!40000 ALTER TABLE `orderdb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdb`
--

DROP TABLE IF EXISTS `userdb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userdb` (
  `email` varchar(40) default NULL,
  `passwd` varchar(32) default NULL,
  `pwdhint` varchar(8) default NULL,
  `fullname` varchar(50) default NULL,
  `role` varchar(1) default NULL,
  `prefcard` varchar(16) default NULL,
  `cardtype` varchar(20) default NULL,
  `expdate` varchar(4) default NULL,
  `cardholdername` varchar(50) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdb`
--

LOCK TABLES `userdb` WRITE;
/*!40000 ALTER TABLE `userdb` DISABLE KEYS */;
INSERT INTO `userdb` VALUES ('AAA_Test_User','098F6BCD4621D373CADE4E832627B4F6','black','Test User','U','-','-','-','-'),('admin','5EBE2294ECD0E0F08EAB7690D2A6EE69','black','Master System Administrator','A','-','-','-','-'),('joe@supplier.com','62072d95acb588c7ee9d6fa0c6c85155','green','Joe Supplier','S','-','-','-','-'),('big@spender.com','9726255eec083aa56dc0449a21b33190','blue','Big Spender','U','-','-','-','-'),('ray@supplier.com','99b0e8da24e29e4ccb5d7d76e677c2ac','red','Ray Supplier','S','-','-','-','-'),('robert@spender.net','e40b34e3380d6d2b238762f0330fbd84','orange','Robert Spender','U','-','-','-','-'),('bill@gander.org','5f4dcc3b5aa765d61d8327deb882cf99','purple','Bill Gander','U','-','-','-','-'),('steve@badstore.net','8cb554127837a4002338c10a299289fb','red','Steve Owner','U','-','-','-','-'),('fred@whole.biz','356c9ee60e9da05301adc3bd96f6b383','yellow','Fred Wholesaler','U','-','-','-','-'),('debbie@supplier.com','2fbd38e6c6c4a64ef43fac3f0be7860e','green','Debby Supplier','S','-','-','-','-'),('mary@spender.com','7f43c1e438dc11a93d19616549d4b701','blue','Mary Spender','U','-','-','-','-'),('sue@spender.com','ea0520bf4d3bd7b9d6ac40c3d63dd500','orange','Sue Spender','U','-','-','-','-'),('curt@customer.com','0DF3DBF0EF9B6F1D49E88194D26AE243','green','Curt Wilson','U','-','-','-','-'),('paul@supplier.com','EB7D34C06CD6B561557D7EF389CDDA3C','red','Paul Rice','S','-','-','-','-'),('kevin@spender.com',NULL,NULL,'Kevin Richards','U','-','-','-','-'),('ryan@badstore.net','40C0BBDC4AEEAA39166825F8B477EDB4','purple','Ryan Shorter','A','-','-','-','-'),('stefan@supplier.com','8E0FAA8363D8EE4D377574AEE8DD992E','yellow','Stefan Drege','S','-','-','-','-'),('landon@whole.biz','29A4F8BFA56D3F970952AFC893355ABC','purple','Landon Scott','U','-','-','-','-'),('sam@customer.net','5EBE2294ECD0E0F08EAB7690D2A6EE69','red','Sam Rahman','U','-','-','-','-'),('david@customer.org','356779A9A1696714480F57FA3FB66D4C','blue','David Myers','U','-','-','-','-'),('john@customer.org','EEE86E9B0FE29B2D63C714B51CE54980','green','John Stiber','U','-','-','-','-'),('tommy@customer.net','7f43c1e438dc11a93d19616549d4b701','orange','Tom O\'Kelley','U','-','-','-','-'),('abhi@abhi.com','d76f3d05cc9ac98f1f9160274a39fe33','green','abhi','U','5000000000000004','Visa','1111','aa'),('rishi@rish.com','ac4b0a568e8d3a14b521eae07006bc95','green','rishi','U','5000000000000004','Master','2121','rishi'),('test@x.com','098f6bcd4621d373cade4e832627b4f6','green','test','U',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `userdb` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-02 11:16:16
