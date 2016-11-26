-- phpMyAdmin SQL Dump
-- version 2.8.0.1
-- http://www.phpmyadmin.net
-- 
-- Host: custsql-pow09
-- Generation Time: Nov 21, 2016 at 09:28 PM
-- Server version: 5.6.32
-- PHP Version: 4.4.9
-- 
-- Database: `davidvandegrift`
-- 

-- --------------------------------------------------------

-- 
-- Table structure for table `semantic_graph_relationships`
-- 
-- Dumping data for table `semantic_graph_relationships`
-- 

INSERT INTO `semantic_graph_relationship` VALUES (1, 1, 3, 'parent', 'categorical structure');
INSERT INTO `semantic_graph_relationship` VALUES (2, 1, 4, 'parent', 'categorical structure');
INSERT INTO `semantic_graph_relationship` VALUES (4, 4, 7, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (5, 4, 6, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (6, 6, 8, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (7, 6, 9, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (8, 8, 10, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (9, 8, 14, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (10, 8, 15, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (11, 10, 11, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (12, 10, 13, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (13, 10, 12, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (14, 9, 17, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (15, 7, 18, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (16, 7, 19, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (17, 7, 20, 'parent', 'categorical structure');
INSERT INTO `semantic_graph_relationship` VALUES (18, 20, 21, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (19, 20, 22, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (20, 20, 23, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (21, 3, 24, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (22, 3, 25, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (23, 3, 27, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (24, 3, 26, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (25, 3, 28, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (26, 3, 29, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (27, 2, 30, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (28, 2, 31, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (29, 2, 32, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (30, 2, 33, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (31, 2, 34, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (32, 2, 35, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (33, 2, 36, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (34, 2, 37, 'parent', 'type');
INSERT INTO `semantic_graph_relationship` VALUES (35, 39, 1, 'topic', 'parent');
INSERT INTO `semantic_graph_relationship` VALUES (36, 1, 40, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (37, 1, 41, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (38, 1, 42, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (39, 1, 43, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (40, 1, 44, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (41, 45, 43, 'type', 'parent');
INSERT INTO `semantic_graph_relationship` VALUES (42, 1, 46, 'parent', 'topic');
INSERT INTO `semantic_graph_relationship` VALUES (43, 1, 48, 'parent', 'topic');
