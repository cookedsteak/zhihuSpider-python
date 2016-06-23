/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50163
 Source Host           : localhost
 Source Database       : zhihu

 Target Server Type    : MySQL
 Target Server Version : 50163
 File Encoding         : utf-8

 Date: 06/23/2016 09:06:01 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `zhihu_users`
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_users`;
CREATE TABLE `zhihu_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'pk',
  `username` varchar(100) DEFAULT NULL COMMENT '链接中的用户名',
  `showname` varchar(120) DEFAULT NULL COMMENT '显示的用户名',
  `followers` int(11) DEFAULT NULL COMMENT '关注人数',
  `followees` int(11) DEFAULT NULL COMMENT '粉',
  `focus` varchar(45) DEFAULT NULL COMMENT '领域',
  `gender` tinyint(2) DEFAULT '1' COMMENT '1male 2female',
  `sign` varchar(255) DEFAULT NULL COMMENT '签名',
  `fr_status` tinyint(4) DEFAULT '0' COMMENT '关注抓取状态',
  `fe_status` tinyint(4) DEFAULT '0' COMMENT '被关注抓取状态',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
