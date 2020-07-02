-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2020 at 06:39 AM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hospitalknit`
--

-- --------------------------------------------------------

--
-- Table structure for table `diagnosticpatient`
--

CREATE TABLE `diagnosticpatient` (
  `id` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `patientId` int(15) NOT NULL,
  `testId` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `diagnosticsmaster`
--

CREATE TABLE `diagnosticsmaster` (
  `testId` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `testName` varchar(35) NOT NULL,
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
  `patientSsnId` int(15) PRIMARY KEY NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `age` int(15) NOT NULL,
  `dateOfAdmission` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `typeOfBed` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL
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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diagnosticpatient`
--
ALTER TABLE `diagnosticpatient`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `diagnosticsmaster`
--
ALTER TABLE `diagnosticsmaster`
  ADD PRIMARY KEY (`testId`);

--
-- Indexes for table `medicinepatient`
--
ALTER TABLE `medicinepatient`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `medicinesmaster`
--
ALTER TABLE `medicinesmaster`
  ADD PRIMARY KEY (`medicineId`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patientId`);

--
-- Indexes for table `userstore`
--
ALTER TABLE `userstore`
  ADD PRIMARY KEY (`userId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diagnosticpatient`
--
ALTER TABLE `diagnosticpatient`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `diagnosticsmaster`
--
ALTER TABLE `diagnosticsmaster`
  MODIFY `testId` int(15) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `medicinepatient`
--
ALTER TABLE `medicinepatient`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `medicinesmaster`
--
ALTER TABLE `medicinesmaster`
  MODIFY `medicineId` int(15) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `patientId` int(15) NOT NULL AUTO_INCREMENT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
