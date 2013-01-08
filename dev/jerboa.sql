-- phpMyAdmin SQL Dump
-- version 2.11.11.3
-- http://www.phpmyadmin.net
--
-- Host: 50.63.239.19
-- Generation Time: Aug 31, 2012 at 10:49 PM
-- Server version: 5.0.92
-- PHP Version: 5.1.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `jerboa`
--

-- --------------------------------------------------------

--
-- Table structure for table `def_mastermodes`
--

DROP TABLE IF EXISTS `def_mastermodes`;
CREATE TABLE `def_mastermodes` (
  `mastermode_id` int(4) NOT NULL,
  `long_name` varchar(16) character set utf8 collate utf8_bin NOT NULL,
  PRIMARY KEY  (`mastermode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `def_mastermodes`
--

INSERT INTO `def_mastermodes` VALUES(0, 'public');
INSERT INTO `def_mastermodes` VALUES(1, 'private');
INSERT INTO `def_mastermodes` VALUES(2, 'match');

-- --------------------------------------------------------

--
-- Table structure for table `def_modes`
--

DROP TABLE IF EXISTS `def_modes`;
CREATE TABLE `def_modes` (
  `mode_id` int(4) NOT NULL,
  `long_name` varchar(32) character set utf8 collate utf8_bin NOT NULL,
  `short_name` varchar(16) character set utf8 collate utf8_bin NOT NULL,
  `team_mode` tinyint(1) NOT NULL,
  `flag_mode` tinyint(1) NOT NULL,
  PRIMARY KEY  (`mode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `def_modes`
--

INSERT INTO `def_modes` VALUES(0, 'team deathmatch', 'tdm', 1, 0);
INSERT INTO `def_modes` VALUES(1, 'co-op edit', 'edit', 0, 0);
INSERT INTO `def_modes` VALUES(2, 'deathmatch', 'dm', 0, 0);
INSERT INTO `def_modes` VALUES(3, 'survivor', 'surv', 0, 0);
INSERT INTO `def_modes` VALUES(4, 'team survivor', 'tsurv', 1, 0);
INSERT INTO `def_modes` VALUES(5, 'capture the flag', 'ctf', 1, 1);
INSERT INTO `def_modes` VALUES(6, 'pistol frenzy', 'pf', 0, 0);
INSERT INTO `def_modes` VALUES(7, 'bot team deathmatch', 'btdm', 1, 0);
INSERT INTO `def_modes` VALUES(8, 'bot deathmatch', 'bdm', 0, 0);
INSERT INTO `def_modes` VALUES(9, 'last swiss standing', 'lss', 0, 0);
INSERT INTO `def_modes` VALUES(10, 'one shot, one kill', 'osok', 0, 0);
INSERT INTO `def_modes` VALUES(11, 'team one shot, one kill', 'tosok', 1, 0);
INSERT INTO `def_modes` VALUES(12, 'bot one show, one  kill', 'bosok', 0, 0);
INSERT INTO `def_modes` VALUES(13, 'hunt the flag', 'htf', 1, 1);
INSERT INTO `def_modes` VALUES(14, 'team keep the flag', 'tktf', 1, 1);
INSERT INTO `def_modes` VALUES(15, 'keep the flag', 'ktf', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `def_teams`
--

DROP TABLE IF EXISTS `def_teams`;
CREATE TABLE `def_teams` (
  `team_id` int(4) NOT NULL,
  `long_name` varchar(32) character set utf8 collate utf8_bin NOT NULL,
  `short_name` varchar(5) character set utf8 collate utf8_bin NOT NULL,
  PRIMARY KEY  (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `def_teams`
--

INSERT INTO `def_teams` VALUES(0, 'cuber liberation army', 'cla');
INSERT INTO `def_teams` VALUES(1, 'rabid viper strike force', 'rvsf');
INSERT INTO `def_teams` VALUES(2, 'cla spectate', 'spect');
INSERT INTO `def_teams` VALUES(3, 'rvsf spectate', 'spect');
INSERT INTO `def_teams` VALUES(4, 'spectate', 'spect');

-- --------------------------------------------------------

--
-- Table structure for table `ss`
--

DROP TABLE IF EXISTS `ss`;
CREATE TABLE `ss` (
  `ss_id` int(16) NOT NULL auto_increment COMMENT 'Unique screenshot id.',
  `user_id` int(10) NOT NULL COMMENT 'User id.',
  `imgur_hash` varchar(32) collate utf8_bin NOT NULL,
  `imgur_delete_hash` varchar(32) collate utf8_bin NOT NULL,
  `timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `title` varchar(64) collate utf8_bin NOT NULL,
  `caption` varchar(128) collate utf8_bin NOT NULL,
  `local_file_path` varchar(256) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`ss_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=199 ;

--
-- Dumping data for table `ss`
--

INSERT INTO `ss` VALUES(185, 20, 'arxvk', 'spwZzFP9z5tfOUA', '2012-08-29 09:57:14', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_16.56.47_ac_arid_TDM.jpg');
INSERT INTO `ss` VALUES(186, 20, 'xZsSN', 'r44tnlgYYv5CfHz', '2012-08-29 10:00:51', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_16.59.38_ac_desert3_CTF.jpg');
INSERT INTO `ss` VALUES(187, 20, 'w1csm', 'mai9I6MOFXSZai9', '2012-08-29 10:00:53', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.00.20_ac_complex_DM.jpg');
INSERT INTO `ss` VALUES(188, 20, '3GPm0', 'KbtSswgZYhX91CT', '2012-08-29 10:00:55', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.00.28_ac_complex_DM.jpg');
INSERT INTO `ss` VALUES(189, 20, 'tsmnc', 'v4oBZd5KIrbchM2', '2012-08-29 10:01:36', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.00.51_ac_outpost_TDM.jpg');
INSERT INTO `ss` VALUES(190, 20, 'QmIDH', 'Wp5YiOwMOvbINld', '2012-08-29 10:01:38', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.00.58_ac_aqueous_BTDM.jpg');
INSERT INTO `ss` VALUES(191, 20, 'opaL2', 'y7Z1fD1WzDoifyx', '2012-08-29 10:01:40', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.01.02_ac_aqueous_BTDM.jpg');
INSERT INTO `ss` VALUES(192, 20, 'HStZf', 'ETYX4xPd0GcANjO', '2012-08-29 10:01:41', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_17.01.09_ac_aqueous_BTDM.jpg');
INSERT INTO `ss` VALUES(193, 20, 'nO2Uh', 'AjvHR5yXDZVGztE', '2012-08-29 12:10:42', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.10.17_ac_desert3_CTF.jpg');
INSERT INTO `ss` VALUES(194, 20, 'gbi1G', '7RAFIOx1Uq5lmDE', '2012-08-29 12:11:31', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.10.28_ac_desert3_CTF.jpg');
INSERT INTO `ss` VALUES(195, 20, 'h09oq', 'cQnMuuLGfHKjZXY', '2012-08-29 12:12:09', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.11.08_ac_desert3_CTF.jpg');
INSERT INTO `ss` VALUES(196, 20, 'sd3YS', 'LDUN77ngBaBNmmo', '2012-08-29 12:12:11', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.11.26_ac_desert3_CTF.jpg');
INSERT INTO `ss` VALUES(197, 20, 'dwdNl', 'fz7UXVJWgpKGt24', '2012-08-29 12:13:00', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.12.14_ac_douze_KTF.jpg');
INSERT INTO `ss` VALUES(198, 20, 'Z0Ad8', 'bvID89qk7sUzG0a', '2012-08-29 12:13:02', 'title', 'caption', 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120829_19.12.34_ac_elevation_KTF.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `ss_meta_blacklist`
--

DROP TABLE IF EXISTS `ss_meta_blacklist`;
CREATE TABLE `ss_meta_blacklist` (
  `ss_id` int(16) NOT NULL,
  `blacklist_name` varchar(64) collate utf8_bin NOT NULL,
  `blacklist_ip` varchar(15) collate utf8_bin NOT NULL,
  `blacklist_reason` varchar(128) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`ss_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `ss_meta_blacklist`
--


-- --------------------------------------------------------

--
-- Table structure for table `ss_meta_players`
--

DROP TABLE IF EXISTS `ss_meta_players`;
CREATE TABLE `ss_meta_players` (
  `ss_id` int(16) NOT NULL,
  `cn` int(2) NOT NULL,
  `flags` int(8) NOT NULL,
  `frags` int(8) NOT NULL,
  `deaths` int(8) NOT NULL,
  `score` int(8) NOT NULL,
  `team_id` int(4) NOT NULL,
  `nick` varchar(16) character set utf8 collate utf8_bin NOT NULL,
  `knife_atk` int(8) NOT NULL,
  `knife_dmg` int(8) NOT NULL,
  `pistol_atk` int(8) NOT NULL,
  `pistol_dmg` int(8) NOT NULL,
  `carbine_atk` int(8) NOT NULL,
  `carbine_dmg` int(8) NOT NULL,
  `shotgun_atk` int(8) NOT NULL,
  `shotgun_dmg` int(8) NOT NULL,
  `smg_atk` int(8) NOT NULL,
  `smg_dmg` int(8) NOT NULL,
  `sniper_atk` int(8) NOT NULL,
  `sniper_dmg` int(8) NOT NULL,
  `assault_atk` int(8) NOT NULL,
  `assault_dmg` int(8) NOT NULL,
  `cpistol_atk` int(8) NOT NULL,
  `cpistol_dmg` int(8) NOT NULL,
  `nade_atk` int(8) NOT NULL,
  `nade_dmg` int(8) NOT NULL,
  `akimbo_atk` int(8) NOT NULL,
  `akimbo_dmg` int(8) NOT NULL,
  KEY `ss_id` (`ss_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ss_meta_players`
--

INSERT INTO `ss_meta_players` VALUES(185, 0, 0, 7, 6, 69, 1, 'kurucutim-turco', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 1, 0, 6, 8, 45, 1, 'una', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 2, 0, 0, 0, 0, 4, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 4, 0, 1, 17, -58, 0, 'fvlo', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 5, 0, 7, 2, 52, 1, 'JKDnaBIKE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 7, 0, 25, 31, 77, 0, '[HKB]Kamikatze', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 11, 0, 18, 26, 68, 0, 'unarmed', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 15, 0, 20, 19, 91, 0, '[HKB]iamnotgood', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 17, 0, 19, 11, 158, 1, 'KAMIKAZE(fr)', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 18, 0, 14, 29, 17, 0, 'akadort', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(185, 19, 0, 35, 19, 326, 1, 'FrenchKiller', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(186, 0, 0, 2, 0, 0, 1, 'SwE|Mos|-', 2, 100, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(186, 1, 0, 3, 2, 37, 1, '=HHG=titidu81', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 80, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(186, 2, 1, 1, 2, 54, 0, 'Sarah-Connor', 0, 0, 0, 0, 0, 0, 2, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(186, 3, 2, 1, 0, 76, 0, 'Rambe', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(186, 4, 0, 0, 0, 0, 0, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(187, 0, 0, 9, 13, 43, 0, 'barrio7', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 24, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(187, 1, 0, 16, 6, 146, 1, 'rikk4rd', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 192, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(187, 2, 0, 0, 0, 0, 0, 'KILLERMAX', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(187, 3, 0, 1, 1, 6, 1, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 72, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(188, 0, 0, 9, 13, 43, 0, 'barrio7', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 24, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(188, 1, 0, 17, 6, 156, 1, 'rikk4rd', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 312, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(188, 2, 0, 0, 1, -4, 0, 'KILLERMAX', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(188, 3, 0, 1, 1, 6, 4, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 72, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(189, 0, 0, 0, 0, 0, 1, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(190, 0, 0, 0, 0, 0, 1, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(190, 1, 0, 0, 0, 0, 1, 'Santa Far', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(190, 2, 0, 0, 0, 0, 0, 'Honey Bunny', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(190, 3, 0, 0, 0, 0, 0, 'luggable', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(191, 0, 0, -1, 0, 0, 1, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(191, 1, 0, 0, 1, 0, 1, 'Santa Far', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(191, 2, 0, 0, 0, 0, 0, 'Honey Bunny', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(191, 3, 0, 0, 0, 0, 0, 'luggable', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(192, 0, 0, -2, 1, 0, 1, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(192, 1, 0, 0, 1, 0, 1, 'Santa Far', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(192, 2, 0, 0, 0, 0, 0, 'Honey Bunny', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(192, 3, 0, 0, 0, 0, 0, 'luggable', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 1, 1, 6, 14, 63, 0, '.44Magnum', 0, 0, 0, 0, 0, 0, 7, 345, 0, 0, 0, 0, 17, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 2, 0, 18, 45, 169, 0, 'noob|gnlscience', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 160, 11, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 3, 0, 8, 15, 67, 0, 'Cloak&Dagger', 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 560, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 4, 3, 20, 17, 432, 1, 'pepe', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 120, 0, 0, 0, 0, 16, 114);
INSERT INTO `ss_meta_players` VALUES(193, 5, 4, 46, 32, 999, 0, 'Trance', 0, 0, 0, 0, 0, 0, 0, 0, 98, 510, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 6, 1, 33, 9, 581, 1, 'Goyo', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 49, 528, 0, 0, 7, 282, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 7, 0, 15, 28, 131, 0, 'BliZzaRd', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 160, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 8, 0, 1, 2, 7, 0, 'jorgp2', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 9, 0, 39, 26, 469, 1, 'SwE|Mos|-', 6, 0, 4, 0, 0, 0, 0, 0, 0, 0, 11, 400, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 10, 0, 3, 14, -1, 1, 'nidhal', 0, 0, 0, 0, 2, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 12, 1, 13, 20, 215, 1, 'BR|_Emicidio', 0, 0, 0, 0, 0, 0, 9, 230, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 13, 0, 14, 7, 222, 1, 'aLovelyNosegey', 0, 0, 0, 0, 0, 0, 5, 360, 46, 255, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 14, 0, 8, 7, 92, 1, 'Drakatch', 0, 0, 0, 0, 0, 0, 6, 325, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 15, 0, -1, 10, -36, 0, 'ayberk', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 96, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 16, 1, 8, 0, 218, 0, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 408, 0, 0, 1, 169, 0, 0);
INSERT INTO `ss_meta_players` VALUES(193, 18, 0, 6, 4, 112, 1, 'povkon!', 0, 0, 0, 0, 0, 0, 8, 155, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 0, 0, 0, 0, 0, 0, 'Edd', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 1, 1, 6, 15, 59, 0, '.44Magnum', 0, 0, 0, 0, 0, 0, 7, 345, 0, 0, 0, 0, 17, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 2, 0, 18, 46, 165, 0, 'noob|gnlscience', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 240, 11, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 3, 0, 10, 15, 112, 0, 'Cloak&Dagger', 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 720, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 4, 3, 20, 17, 444, 1, 'pepe', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 120, 0, 0, 0, 0, 16, 114);
INSERT INTO `ss_meta_players` VALUES(194, 5, 4, 46, 33, 995, 0, 'Trance', 0, 0, 0, 0, 0, 0, 0, 0, 103, 510, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 6, 1, 36, 10, 631, 1, 'Goyo', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 74, 768, 0, 0, 8, 466, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 7, 0, 15, 28, 127, 0, 'BliZzaRd', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 160, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 8, 0, 1, 2, 7, 0, 'jorgp2', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 9, 0, 40, 27, 503, 1, 'SwE|Mos|-', 6, 0, 7, 36, 0, 0, 0, 0, 0, 0, 12, 480, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 10, 0, 3, 14, -1, 1, 'nidhal', 0, 0, 0, 0, 4, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 12, 1, 13, 20, 215, 1, 'BR|_Emicidio', 0, 0, 0, 0, 0, 0, 10, 270, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 13, 0, 16, 8, 289, 1, 'aLovelyNosegey', 0, 0, 0, 0, 0, 0, 9, 645, 46, 255, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 14, 0, 8, 7, 92, 1, 'Drakatch', 0, 0, 0, 0, 0, 0, 6, 325, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 15, 0, -1, 12, -44, 0, 'ayberk', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 96, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 16, 1, 8, 1, 214, 0, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 408, 0, 0, 1, 169, 0, 0);
INSERT INTO `ss_meta_players` VALUES(194, 18, 0, 5, 4, 92, 1, 'povkon!', 0, 0, 0, 0, 0, 0, 8, 155, 0, 0, 0, 0, 0, 0, 0, 0, 4, 141, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 0, 0, 1, 1, 7, 0, 'Edd', 0, 0, 0, 0, 8, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 1, 1, 6, 17, 51, 0, '.44Magnum', 0, 0, 0, 0, 4, 0, 9, 385, 0, 0, 0, 0, 17, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 2, 0, 19, 47, 185, 0, 'noob|gnlscience', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 400, 11, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 3, 0, 14, 18, 176, 0, 'Cloak&Dagger', 11, 150, 0, 0, 0, 0, 0, 0, 0, 0, 16, 800, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 4, 3, 20, 19, 436, 1, 'pepe', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 192, 0, 0, 0, 0, 16, 114);
INSERT INTO `ss_meta_players` VALUES(195, 5, 4, 49, 35, 1045, 0, 'Trance', 0, 0, 0, 0, 0, 0, 0, 0, 163, 750, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 6, 1, 38, 11, 652, 1, 'Goyo', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 1176, 0, 0, 12, 474, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 7, 0, 15, 29, 123, 0, 'BliZzaRd', 12, 0, 0, 0, 0, 0, 0, 0, 31, 105, 6, 160, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 8, 0, 1, 2, 7, 0, 'jorgp2', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 9, 0, 0, 0, 0, 1, 'Deka!', 0, 0, 0, 0, 0, 0, 2, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 10, 0, 5, 16, 11, 1, 'nidhal', 0, 0, 0, 0, 19, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 12, 1, 15, 21, 255, 1, 'BR|_Emicidio', 0, 0, 0, 0, 0, 0, 15, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 13, 0, 19, 10, 355, 1, 'aLovelyNosegey', 0, 0, 0, 0, 0, 0, 16, 925, 46, 255, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 14, 0, 9, 8, 115, 1, 'Drakatch', 0, 0, 0, 0, 0, 0, 16, 545, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 15, 0, -1, 13, -48, 0, 'ayberk', 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 144, 0, 0, 0, 0, 25, 76);
INSERT INTO `ss_meta_players` VALUES(195, 16, 1, 11, 3, 286, 0, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 816, 0, 0, 1, 169, 0, 0);
INSERT INTO `ss_meta_players` VALUES(195, 18, 0, 8, 6, 133, 1, 'povkon!', 0, 0, 0, 0, 0, 0, 17, 595, 0, 0, 0, 0, 0, 0, 0, 0, 4, 141, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 0, 0, 1, 2, 3, 0, 'Edd', 0, 0, 0, 0, 12, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 1, 1, 7, 18, 69, 0, '.44Magnum', 0, 0, 0, 0, 4, 0, 12, 535, 0, 0, 0, 0, 17, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 2, 0, 19, 47, 185, 0, 'noob|gnlscience', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 400, 11, 120, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 3, 0, 16, 19, 194, 0, 'Cloak&Dagger', 11, 150, 0, 0, 0, 0, 0, 0, 0, 0, 19, 960, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 4, 3, 20, 20, 432, 1, 'pepe', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 52, 264, 0, 0, 0, 0, 16, 114);
INSERT INTO `ss_meta_players` VALUES(196, 5, 4, 52, 35, 1093, 0, 'Trance', 0, 0, 0, 0, 0, 0, 0, 0, 195, 975, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 6, 1, 40, 12, 668, 1, 'Goyo', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 141, 1368, 0, 0, 12, 474, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 7, 0, 15, 29, 123, 0, 'BliZzaRd', 14, 50, 0, 0, 0, 0, 0, 0, 31, 105, 6, 160, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 8, 0, 1, 2, 7, 0, 'jorgp2', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 9, 0, 1, 1, 6, 1, 'Deka!', 0, 0, 0, 0, 0, 0, 4, 170, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 10, 0, 6, 17, 17, 1, 'nidhal', 0, 0, 0, 0, 22, 420, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 12, 1, 15, 22, 251, 1, 'BR|_Emicidio', 0, 0, 0, 0, 0, 0, 16, 545, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 13, 0, 19, 10, 355, 1, 'aLovelyNosegey', 0, 0, 0, 0, 0, 0, 17, 925, 46, 255, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 15, 0, -1, 14, -52, 0, 'ayberk', 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 144, 0, 0, 0, 0, 25, 76);
INSERT INTO `ss_meta_players` VALUES(196, 16, 1, 12, 3, 296, 0, 'HyPE|gdm', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 141, 960, 0, 0, 1, 169, 0, 0);
INSERT INTO `ss_meta_players` VALUES(196, 18, 0, 8, 7, 141, 1, 'povkon!', 0, 0, 0, 0, 0, 0, 19, 610, 0, 0, 0, 0, 0, 0, 0, 0, 6, 144, 0, 0);
INSERT INTO `ss_meta_players` VALUES(197, 0, 3, 10, 28, 50, 1, 'manon', 2, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(197, 1, 0, 29, 28, 173, 0, 'daxter', 0, 0, 0, 0, 0, 0, 3, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(197, 2, 5, 36, 27, 333, 1, 'Darkell', 0, 0, 13, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(197, 3, 0, 1, 0, 15, 0, 'HyPE|GDM', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 96, 0, 0, 1, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(198, 0, 0, 0, 0, 0, 1, 'manon', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(198, 1, 0, 0, 0, 0, 0, 'daxter', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `ss_meta_players` VALUES(198, 2, 0, 1, 0, 15, 1, 'Darkell', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 114);
INSERT INTO `ss_meta_players` VALUES(198, 3, 0, 0, 1, -4, 4, 'HyPE|GDM', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ss_meta_server`
--

DROP TABLE IF EXISTS `ss_meta_server`;
CREATE TABLE `ss_meta_server` (
  `ss_id` int(16) NOT NULL,
  `ip` varchar(64) collate utf8_bin NOT NULL,
  `port` varchar(5) collate utf8_bin NOT NULL,
  `hostname` varchar(253) collate utf8_bin NOT NULL,
  `map` varchar(128) collate utf8_bin NOT NULL,
  `mode_id` int(4) NOT NULL,
  `mastermode_id` int(4) NOT NULL,
  `minutes_remaining` int(4) NOT NULL,
  PRIMARY KEY  (`ss_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `ss_meta_server`
--

INSERT INTO `ss_meta_server` VALUES(185, '88.191.126.218', '6600', 'sd-22753.dedibox.fr', 'ac_arid', 0, 0, 5);
INSERT INTO `ss_meta_server` VALUES(186, '88.191.129.31', '28763', 'procrastin.at', 'ac_desert3', 5, 0, 11);
INSERT INTO `ss_meta_server` VALUES(187, '62.75.210.97', '28763', 'ej3416.de', 'ac_complex', 2, 0, 3);
INSERT INTO `ss_meta_server` VALUES(188, '62.75.210.97', '28763', 'ej3416.de', 'ac_complex', 2, 0, 3);
INSERT INTO `ss_meta_server` VALUES(189, '', '', '', 'ac_outpost', 0, 0, 0);
INSERT INTO `ss_meta_server` VALUES(190, '', '', '', 'ac_aqueous', 7, 0, 15);
INSERT INTO `ss_meta_server` VALUES(191, '', '', '', 'ac_aqueous', 7, 0, 15);
INSERT INTO `ss_meta_server` VALUES(192, '', '', '', 'ac_aqueous', 7, 0, 15);
INSERT INTO `ss_meta_server` VALUES(193, '78.46.116.16', '20030', 'de.mysick.tk', 'ac_desert3', 5, 0, 2);
INSERT INTO `ss_meta_server` VALUES(194, '78.46.116.16', '20030', 'de.mysick.tk', 'ac_desert3', 5, 0, 1);
INSERT INTO `ss_meta_server` VALUES(195, '78.46.116.16', '20030', 'de.mysick.tk', 'ac_desert3', 5, 0, 1);
INSERT INTO `ss_meta_server` VALUES(196, '78.46.116.16', '20030', 'de.mysick.tk', 'ac_desert3', 5, 0, 0);
INSERT INTO `ss_meta_server` VALUES(197, '103.6.213.144', '22222', '103.6.213.144', 'ac_douze', 15, 0, 0);
INSERT INTO `ss_meta_server` VALUES(198, '103.6.213.144', '22222', '103.6.213.144', 'ac_elevation', 15, 0, 10);

-- --------------------------------------------------------

--
-- Table structure for table `ss_meta_tagged`
--

DROP TABLE IF EXISTS `ss_meta_tagged`;
CREATE TABLE `ss_meta_tagged` (
  `ss_id` int(16) NOT NULL,
  `tag_id` int(16) NOT NULL,
  UNIQUE KEY `ss_id` (`ss_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `ss_meta_tagged`
--


-- --------------------------------------------------------

--
-- Table structure for table `ss_tags`
--

DROP TABLE IF EXISTS `ss_tags`;
CREATE TABLE `ss_tags` (
  `tag_id` int(16) NOT NULL auto_increment,
  `text` varchar(64) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`tag_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=8 ;

--
-- Dumping data for table `ss_tags`
--

INSERT INTO `ss_tags` VALUES(7, 'blacklist');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) NOT NULL auto_increment,
  `nick` varchar(32) collate utf8_bin NOT NULL,
  `email` varchar(128) collate utf8_bin NOT NULL,
  `password_hash` varchar(60) collate utf8_bin NOT NULL,
  `salt` varchar(5) collate utf8_bin NOT NULL,
  `activation_key` varchar(32) collate utf8_bin NOT NULL,
  `activated` tinyint(1) NOT NULL default '0',
  `upload_key` varchar(8) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`user_id`),
  UNIQUE KEY `nick` (`nick`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=31 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` VALUES(20, 'gdm', 'gdm.jerboa@gmail.com', '$2a$08$RAz5TiyWvsbuamnfK6iF6.dDf7qb7EZonqnetJ4rid83SYiAXlzYS', '402f2', 'ohfylxGqZG01GGukKZKDYToamCxhf78X', 1, 'IWgvMAy8');
