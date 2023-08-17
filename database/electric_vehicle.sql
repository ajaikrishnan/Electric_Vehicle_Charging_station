-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 02, 2023 at 09:15 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `electric_vehicle`
--

-- --------------------------------------------------------

--
-- Table structure for table `ev_booking`
--

CREATE TABLE `ev_booking` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `station` varchar(30) NOT NULL,
  `carno` varchar(20) NOT NULL,
  `reserve` varchar(20) NOT NULL,
  `slot` int(11) NOT NULL,
  `cimage` varchar(20) NOT NULL,
  `mins` int(11) NOT NULL,
  `plan` int(11) NOT NULL,
  `amount` double NOT NULL,
  `rtime` varchar(20) NOT NULL,
  `etime` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `edate` varchar(15) NOT NULL,
  `otp` varchar(10) NOT NULL,
  `charge` double NOT NULL,
  `charge_time` int(11) NOT NULL,
  `charge_min` int(11) NOT NULL,
  `charge_sec` int(11) NOT NULL,
  `charge_st` int(11) NOT NULL,
  `pay_mode` varchar(20) NOT NULL,
  `pay_st` int(11) NOT NULL,
  `sms_st` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_booking`
--

INSERT INTO `ev_booking` (`id`, `uname`, `station`, `carno`, `reserve`, `slot`, `cimage`, `mins`, `plan`, `amount`, `rtime`, `etime`, `rdate`, `edate`, `otp`, `charge`, `charge_time`, `charge_min`, `charge_sec`, `charge_st`, `pay_mode`, `pay_st`, `sms_st`, `status`) VALUES
(1, 'rahul', '1', 'TN2223', '1', 3, 'evch.jpg', 0, 2, 200, '19:58:44', '20:07:19', '02-01-2023', '02-01-2023', '2701', 200, 30, 0, 60, 3, 'Bank', 2, 0, 3);

-- --------------------------------------------------------

--
-- Table structure for table `ev_register`
--

CREATE TABLE `ev_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `account` varchar(20) NOT NULL,
  `card` varchar(20) NOT NULL,
  `bank` varchar(20) NOT NULL,
  `amount` double NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_register`
--

INSERT INTO `ev_register` (`id`, `name`, `address`, `mobile`, `email`, `account`, `card`, `bank`, `amount`, `uname`, `pass`) VALUES
(1, 'Rahul', 'Salem', 6381082863, 'rahul@gmail.com', '2200774433', '270600042828', 'SBI', 10000, 'rahul', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `ev_station`
--

CREATE TABLE `ev_station` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `stype` varchar(20) NOT NULL,
  `num_charger` int(11) NOT NULL,
  `area` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `lat` varchar(20) NOT NULL,
  `lon` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_station`
--

INSERT INTO `ev_station` (`id`, `name`, `stype`, `num_charger`, `area`, `city`, `lat`, `lon`, `uname`, `pass`) VALUES
(1, 'evstation', 'Private', 10, 'SS Nagar', 'Salem', '10.8315', '78.5993', 'evstation', '123456');
