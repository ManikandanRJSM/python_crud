-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 09, 2020 at 09:46 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cruddb`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_email` varchar(50) NOT NULL,
  `user_password` varchar(100) NOT NULL,
  `password_raw` varchar(200) DEFAULT NULL,
  `user_profile` varchar(100) DEFAULT NULL,
  `user_role` enum('1','2','3') DEFAULT NULL COMMENT '1-admin,2-users,3-guest',
  `status` enum('1','2','3','4') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `password_raw`, `user_profile`, `user_role`, `status`) VALUES
(1, 'admin', 'admin@gmail.com', '', '12345', NULL, '1', '1'),
(2, 'mani', 'mani@gmail.com', 'pbkdf2:sha256:150000$tX6FOvGq$9ee9e10ebf4b9ac1c1fe9b9c8c9ac16509d7e4a64ba2e4baa98d448b5343bc02', '123', NULL, '2', '1'),
(3, 'user', 'user@gmail.com', 'pbkdf2:sha256:150000$ooAQKDBE$91f7c1555ea8678104b8469229ef75c0c6d05dad18954a7e8c9d01db6a4c493a', '123', 'Screenshot_4.png', '2', '1'),
(4, 'harry kane', 'kane@gmail.com', 'pbkdf2:sha256:150000$UWxJOt8C$17df5816b0c04948932aed3b4e7a980c726a8843184eb67819453e23ddc680d6', 'asd', 'taxiwaala-songs-download-vijay-devarakonda.jpg', '2', '1'),
(5, 'auba ', 'auba@gmail.com', 'pbkdf2:sha256:150000$2bviqcR6$0f7266878bb5644e08f032cf83f474f09ce4c82dc1991bf470a3594c58b9cf25', 'bvb', 'Screenshot_4.png', '1', '1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
