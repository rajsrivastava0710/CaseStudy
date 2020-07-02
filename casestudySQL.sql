--
-- Database: 'knit_hms`
--
-- Use all these queries before starting the application
-- Change the sql password in __init.py__
-- --------------------------------------------------------

-- create database

CREATE DATABASE knit_hms;
USE knit_hms;
--
-- Table structure for table `diagnosticpatient`
--

CREATE TABLE `diagnosticpatient` (
  `id` int(9) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `patientId` int(15) NOT NULL,
  `testId` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `diagnosticsmaster`
--

CREATE TABLE `diagnosticsmaster` (
  `testId` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `testName` varchar(50) NOT NULL,
  `testCharge` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `medicinepatient`
--

CREATE TABLE `medicinepatient` (
  `patientId` int(15) NOT NULL,
  `medicineId` int(15) NOT NULL,
  `quantityIssued` int(15) NOT NULL,
  `id` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `medicinesmaster`
--

CREATE TABLE `medicinesmaster` (
  `medicineId` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `medicineName` varchar(255) NOT NULL,
  `quantityAvailable` int(15) NOT NULL,
  `rateOfMedicine` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patientSsnId` int(9) PRIMARY KEY NOT NULL,
  `patientId` int(9) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `age` int(15) NOT NULL,
  `dateOfAdmission` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `typeOfBed` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `dateOfDischarge` TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `userstore`
--

CREATE TABLE `userstore` (
  `login` varchar(255) NOT NULL PRIMARY KEY,
  `password` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Admin Data
--

INSERT INTO userstore(login,password) VALUES('admin@tcs.com','tcs_knit');

-- --------------------------------------------------------

--
-- Medicine Entry
--

INSERT INTO medicinesmaster(medicineName,quantityAvailable,rateOfMedicine)
VALUES('Disprin',18,10),('Paracetamol',98,5),('Insulin',30,75),('Combeflam',180,4);


-- --------------------------------------------------------

--
-- Diagnostic Data
--

INSERT INTO diagnosticsmaster(testName,testCharge)
VALUES('Corona',20000),('Swine Flue',4000),('X Ray',500),('Blood Test',5000);

-- --------------------------------------------------------

--
--DONE
--