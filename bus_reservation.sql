-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 04, 2022 at 05:31 PM
-- Server version: 5.7.26
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bus_reservation`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
CREATE TABLE IF NOT EXISTS `booking` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `payment` float NOT NULL,
  `booking_date` date DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_booking_user_id_users_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `user_id`, `description`, `payment`, `booking_date`, `status`) VALUES
(1, 1, NULL, 21, '2022-07-05', 1),
(2, 1, NULL, 21, '2022-07-05', 0),
(3, 1, NULL, 14, '2022-07-05', 0);

-- --------------------------------------------------------

--
-- Table structure for table `booking_detail`
--

DROP TABLE IF EXISTS `booking_detail`;
CREATE TABLE IF NOT EXISTS `booking_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) NOT NULL,
  `trip_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `seat_id` int(11) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_booking_detail_trip_trip_id` (`trip_id`),
  KEY `fk_booking_detail_booking_booking_id` (`booking_id`),
  KEY `seat_id` (`seat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking_detail`
--

INSERT INTO `booking_detail` (`id`, `booking_id`, `trip_id`, `description`, `seat_id`, `price`) VALUES
(1, 1, 1, NULL, 1, 7),
(2, 1, 1, NULL, 6, 7),
(3, 1, 1, NULL, 8, 7),
(4, 2, 1, NULL, 2, 7),
(5, 2, 1, NULL, 7, 7),
(6, 2, 1, NULL, 15, 7),
(7, 3, 2, NULL, 16, 7),
(8, 3, 2, NULL, 17, 7);

-- --------------------------------------------------------

--
-- Table structure for table `bus`
--

DROP TABLE IF EXISTS `bus`;
CREATE TABLE IF NOT EXISTS `bus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `bus_name` varchar(255) NOT NULL,
  `loc_id` int(11) NOT NULL,
  `bus_desc` varchar(255) DEFAULT NULL,
  `num_of_seat` int(11) DEFAULT '15',
  `price` float DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_bus_bus_type_type_id` (`type_id`),
  KEY `fk_locations_bus_loc_id` (`loc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bus`
--

INSERT INTO `bus` (`id`, `type_id`, `bus_name`, `loc_id`, `bus_desc`, `num_of_seat`, `price`, `created_date`, `status`) VALUES
(1, 1, 'PP-SR-Express-1', 1, NULL, 15, 7, '2022-06-15 12:40:57', 0),
(2, 1, 'PP-SR-Express-2', 1, NULL, 15, 7, '2022-06-15 12:41:14', 0),
(3, 2, 'PP-SR-VIP', 1, NULL, 15, 10, '2022-06-15 12:42:05', 1),
(4, 1, 'PP-SHV-Express-1', 3, NULL, 15, 7, '2022-06-15 12:42:46', 1),
(5, 1, 'PP-SHV-Express-2', 3, NULL, 15, 7, '2022-06-15 12:42:54', 1),
(6, 2, 'PP-SHV-VIP', 3, NULL, 15, 10, '2022-06-15 12:43:13', 1),
(7, 1, 'SR-PP-Express-1', 2, NULL, 15, 7, '2022-06-26 23:06:29', 1),
(8, 1, 'SR-PP-Express-2', 2, NULL, 15, 7, '2022-06-26 23:06:34', 1),
(9, 2, 'SR-PP-VIP', 2, NULL, 15, 10, '2022-06-26 23:06:51', 1),
(10, 1, 'SHV-PP-Express-1', 4, NULL, 15, 7, '2022-06-26 23:07:06', 1),
(11, 1, 'SHV-PP-Express-2', 4, NULL, 15, 7, '2022-06-26 23:07:08', 1),
(12, 2, 'SHV-PP-VIP', 4, NULL, 15, 10, '2022-06-26 23:07:21', 1);

-- --------------------------------------------------------

--
-- Table structure for table `bus_seat`
--

DROP TABLE IF EXISTS `bus_seat`;
CREATE TABLE IF NOT EXISTS `bus_seat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bus_id` int(11) NOT NULL,
  `seat_name` varchar(255) DEFAULT NULL,
  `seat_desc` varchar(255) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_bus_seat_bus_id_bus_id` (`bus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=181 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bus_seat`
--

INSERT INTO `bus_seat` (`id`, `bus_id`, `seat_name`, `seat_desc`, `status`) VALUES
(1, 1, '1', NULL, 0),
(2, 1, '2', NULL, 0),
(3, 1, '3', NULL, 1),
(4, 1, '4', NULL, 1),
(5, 1, '5', NULL, 1),
(6, 1, '6', NULL, 0),
(7, 1, '7', NULL, 0),
(8, 1, '8', NULL, 0),
(9, 1, '9', NULL, 1),
(10, 1, '10', NULL, 1),
(11, 1, '11', NULL, 1),
(12, 1, '12', NULL, 1),
(13, 1, '13', NULL, 1),
(14, 1, '14', NULL, 1),
(15, 1, '15', NULL, 0),
(16, 2, '1', NULL, 0),
(17, 2, '2', NULL, 0),
(18, 2, '3', NULL, 1),
(19, 2, '4', NULL, 1),
(20, 2, '5', NULL, 1),
(21, 2, '6', NULL, 1),
(22, 2, '7', NULL, 1),
(23, 2, '8', NULL, 1),
(24, 2, '9', NULL, 1),
(25, 2, '10', NULL, 1),
(26, 2, '11', NULL, 1),
(27, 2, '12', NULL, 1),
(28, 2, '13', NULL, 1),
(29, 2, '14', NULL, 1),
(30, 2, '15', NULL, 1),
(31, 3, '1', NULL, 1),
(32, 3, '2', NULL, 1),
(33, 3, '3', NULL, 1),
(34, 3, '4', NULL, 1),
(35, 3, '5', NULL, 1),
(36, 3, '6', NULL, 1),
(37, 3, '7', NULL, 1),
(38, 3, '8', NULL, 1),
(39, 3, '9', NULL, 1),
(40, 3, '10', NULL, 1),
(41, 3, '11', NULL, 1),
(42, 3, '12', NULL, 1),
(43, 3, '13', NULL, 1),
(44, 3, '14', NULL, 1),
(45, 3, '15', NULL, 1),
(46, 4, '1', NULL, 1),
(47, 4, '2', NULL, 1),
(48, 4, '3', NULL, 1),
(49, 4, '4', NULL, 1),
(50, 4, '5', NULL, 1),
(51, 4, '6', NULL, 1),
(52, 4, '7', NULL, 1),
(53, 4, '8', NULL, 1),
(54, 4, '9', NULL, 1),
(55, 4, '10', NULL, 1),
(56, 4, '11', NULL, 1),
(57, 4, '12', NULL, 1),
(58, 4, '13', NULL, 1),
(59, 4, '14', NULL, 1),
(60, 4, '15', NULL, 1),
(61, 5, '1', NULL, 1),
(62, 5, '2', NULL, 1),
(63, 5, '3', NULL, 1),
(64, 5, '4', NULL, 1),
(65, 5, '5', NULL, 1),
(66, 5, '6', NULL, 1),
(67, 5, '7', NULL, 1),
(68, 5, '8', NULL, 1),
(69, 5, '9', NULL, 1),
(70, 5, '10', NULL, 1),
(71, 5, '11', NULL, 1),
(72, 5, '12', NULL, 1),
(73, 5, '13', NULL, 1),
(74, 5, '14', NULL, 1),
(75, 5, '15', NULL, 1),
(76, 6, '1', NULL, 1),
(77, 6, '2', NULL, 1),
(78, 6, '3', NULL, 1),
(79, 6, '4', NULL, 1),
(80, 6, '5', NULL, 1),
(81, 6, '6', NULL, 1),
(82, 6, '7', NULL, 1),
(83, 6, '8', NULL, 1),
(84, 6, '9', NULL, 1),
(85, 6, '10', NULL, 1),
(86, 6, '11', NULL, 1),
(87, 6, '12', NULL, 1),
(88, 6, '13', NULL, 1),
(89, 6, '14', NULL, 1),
(90, 6, '15', NULL, 1),
(91, 7, '1', NULL, 1),
(92, 7, '2', NULL, 1),
(93, 7, '3', NULL, 1),
(94, 7, '4', NULL, 1),
(95, 7, '5', NULL, 1),
(96, 7, '6', NULL, 1),
(97, 7, '7', NULL, 1),
(98, 7, '8', NULL, 1),
(99, 7, '9', NULL, 1),
(100, 7, '10', NULL, 1),
(101, 7, '11', NULL, 1),
(102, 7, '12', NULL, 1),
(103, 7, '13', NULL, 1),
(104, 7, '14', NULL, 1),
(105, 7, '15', NULL, 1),
(106, 8, '1', NULL, 1),
(107, 8, '2', NULL, 1),
(108, 8, '3', NULL, 1),
(109, 8, '4', NULL, 1),
(110, 8, '5', NULL, 1),
(111, 8, '6', NULL, 1),
(112, 8, '7', NULL, 1),
(113, 8, '8', NULL, 1),
(114, 8, '9', NULL, 1),
(115, 8, '10', NULL, 1),
(116, 8, '11', NULL, 1),
(117, 8, '12', NULL, 1),
(118, 8, '13', NULL, 1),
(119, 8, '14', NULL, 1),
(120, 8, '15', NULL, 1),
(121, 9, '1', NULL, 1),
(122, 9, '2', NULL, 1),
(123, 9, '3', NULL, 1),
(124, 9, '4', NULL, 1),
(125, 9, '5', NULL, 1),
(126, 9, '6', NULL, 1),
(127, 9, '7', NULL, 1),
(128, 9, '8', NULL, 1),
(129, 9, '9', NULL, 1),
(130, 9, '10', NULL, 1),
(131, 9, '11', NULL, 1),
(132, 9, '12', NULL, 1),
(133, 9, '13', NULL, 1),
(134, 9, '14', NULL, 1),
(135, 9, '15', NULL, 1),
(136, 10, '1', NULL, 1),
(137, 10, '2', NULL, 1),
(138, 10, '3', NULL, 1),
(139, 10, '4', NULL, 1),
(140, 10, '5', NULL, 1),
(141, 10, '6', NULL, 1),
(142, 10, '7', NULL, 1),
(143, 10, '8', NULL, 1),
(144, 10, '9', NULL, 1),
(145, 10, '10', NULL, 1),
(146, 10, '11', NULL, 1),
(147, 10, '12', NULL, 1),
(148, 10, '13', NULL, 1),
(149, 10, '14', NULL, 1),
(150, 10, '15', NULL, 1),
(151, 11, '1', NULL, 1),
(152, 11, '2', NULL, 1),
(153, 11, '3', NULL, 1),
(154, 11, '4', NULL, 1),
(155, 11, '5', NULL, 1),
(156, 11, '6', NULL, 1),
(157, 11, '7', NULL, 1),
(158, 11, '8', NULL, 1),
(159, 11, '9', NULL, 1),
(160, 11, '10', NULL, 1),
(161, 11, '11', NULL, 1),
(162, 11, '12', NULL, 1),
(163, 11, '13', NULL, 1),
(164, 11, '14', NULL, 1),
(165, 11, '15', NULL, 1),
(166, 12, '1', NULL, 1),
(167, 12, '2', NULL, 1),
(168, 12, '3', NULL, 1),
(169, 12, '4', NULL, 1),
(170, 12, '5', NULL, 1),
(171, 12, '6', NULL, 1),
(172, 12, '7', NULL, 1),
(173, 12, '8', NULL, 1),
(174, 12, '9', NULL, 1),
(175, 12, '10', NULL, 1),
(176, 12, '11', NULL, 1),
(177, 12, '12', NULL, 1),
(178, 12, '13', NULL, 1),
(179, 12, '14', NULL, 1),
(180, 12, '15', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `bus_type`
--

DROP TABLE IF EXISTS `bus_type`;
CREATE TABLE IF NOT EXISTS `bus_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bus_type`
--

INSERT INTO `bus_type` (`id`, `type_name`, `created_at`, `status`) VALUES
(1, 'Express', '2022-06-14 22:43:19', 1),
(2, 'VIP', '2022-06-14 22:43:30', 1);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
CREATE TABLE IF NOT EXISTS `locations` (
  `loc_id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_name` varchar(255) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`loc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`loc_id`, `loc_name`, `created_date`, `status`) VALUES
(1, 'Phnom Penh to Siem Reap', '2022-03-25', 1),
(2, 'Siem Reap to Phnom Penh', '2022-03-25', 1),
(3, 'Phnom Penh to Sihanoukville', '2022-03-25', 1),
(4, 'Sihanoukville to Phnom Penh', '2022-03-25', 1);

-- --------------------------------------------------------

--
-- Table structure for table `payment_offline`
--

DROP TABLE IF EXISTS `payment_offline`;
CREATE TABLE IF NOT EXISTS `payment_offline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `booking_date` date NOT NULL,
  `pay_date` date DEFAULT NULL,
  `cus_id` int(11) NOT NULL,
  `pay_status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `booking_id` (`booking_id`),
  KEY `cus_id` (`cus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `payment_offline`
--

INSERT INTO `payment_offline` (`id`, `booking_id`, `description`, `booking_date`, `pay_date`, `cus_id`, `pay_status`) VALUES
(1, 2, NULL, '2022-07-05', NULL, 1, 0),
(2, 3, NULL, '2022-07-05', NULL, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `payment_online`
--

DROP TABLE IF EXISTS `payment_online`;
CREATE TABLE IF NOT EXISTS `payment_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `pay_date` date DEFAULT NULL,
  `cus_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_payment_online_booking_booking_id` (`booking_id`),
  KEY `fk_payment_paydate_booking_booking_date` (`pay_date`),
  KEY `fk_payment_online_cus_id_users_user_id` (`cus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `payment_online`
--

INSERT INTO `payment_online` (`id`, `booking_id`, `description`, `pay_date`, `cus_id`) VALUES
(1, 1, NULL, '2022-07-05', 1);

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) NOT NULL,
  `role_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`id`, `role_name`, `role_desc`) VALUES
(1, 'Admin', NULL),
(2, 'User', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `trip`
--

DROP TABLE IF EXISTS `trip`;
CREATE TABLE IF NOT EXISTS `trip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_id` int(11) NOT NULL,
  `bus_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `seat` int(11) DEFAULT '15',
  `departure_date` date NOT NULL,
  `departure_time` time DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_trip_locations_loc_id` (`loc_id`),
  KEY `fk_trip_bus_id_bus_id` (`bus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `trip`
--

INSERT INTO `trip` (`id`, `loc_id`, `bus_id`, `description`, `seat`, `departure_date`, `departure_time`, `created_at`, `updated_at`, `status`) VALUES
(1, 1, 1, NULL, 15, '2022-07-04', '08:00:00', '2022-06-28 12:32:01', '2022-07-04 09:32:39', 1),
(2, 1, 2, NULL, 15, '2022-07-04', '08:00:00', '2022-06-29 15:06:41', '2022-07-04 09:32:54', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `user_pass` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL DEFAULT '2',
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `user_desc` varchar(255),
  `phone` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_pass`, `role_id`, `first_name`, `last_name`, `date_of_birth`, `user_desc`, `phone`, `email`, `created_date`, `status`) VALUES
(1, 'socheapheaktra', 'pheaktra123', 2, 'Doung', 'Socheapheaktra', '2001-01-23', 'User', '092605441', 'socheapheaktra@gmail.com', '2022-04-09', 1),
(2, 'socheapheaktra_test', 'pheaktra123', 2, 'Socheapheaktra', 'Test', NULL, 'User', NULL, 'socheapheaktra_test@gmail.com', '2022-04-11', 1),
(7, 'test_user', '123456', 2, NULL, NULL, NULL, 'User', NULL, 'test@test.com', '2022-04-04', 1),
(4, 'admin', 'admin', 1, NULL, NULL, NULL, 'Admin', NULL, 'socheapheaktra_admin@gmail.com', '2022-04-20', 1),
(6, 'socheapheaktra123', 'pheaktra123', 2, NULL, NULL, NULL, 'User', NULL, 'socheapheaktra@gmail.com', '2022-04-25', 1),
(11, 'socheapheaktra1', 'pheaktra123', 2, NULL, NULL, NULL, 'User', NULL, 'socheapheaktra1@gmail.com', NULL, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
