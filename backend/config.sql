-- -----------------------------------------------------
-- Schema config
-- -----------------------------------------------------

CREATE database IF NOT EXISTS `download` DEFAULT CHARACTER SET utf8mb4 ;
USE `download` ;

-- -----------------------------------------------------
-- Create users
-- -----------------------------------------------------
DROP USER IF EXISTS `agoda`@'%';
CREATE USER `agoda`@'%' IDENTIFIED BY 'Snx@D3fault';
GRANT ALL PRIVILEGES ON `download`.* TO `agoda`@'%';

-- -----------------------------------------------------
-- Table structure for table `data`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_source` varchar(500) NOT NULL,
  `file_destination` varchar(500) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `protocol` varchar(100) NOT NULL,
  `data_type` varchar(100) NOT NULL,
  `download_speed` varchar(50) NOT NULL,
  `failure_percentage` varchar(50) NOT NULL,
  `status` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

-- -----------------------------------------------------
-- Dumping data for table `data`
-- -----------------------------------------------------
