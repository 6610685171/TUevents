-- MySQL dump 10.13  Distrib 9.0.1, for macos14.7 (x86_64)
--
-- Host: localhost    Database: tuevents_2024
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add announcement',7,'add_announcement'),(26,'Can change announcement',7,'change_announcement'),(27,'Can delete announcement',7,'delete_announcement'),(28,'Can view announcement',7,'view_announcement'),(29,'Can add club',8,'add_club'),(30,'Can change club',8,'change_club'),(31,'Can delete club',8,'delete_club'),(32,'Can view club',8,'view_club'),(33,'Can add found',9,'add_found'),(34,'Can change found',9,'change_found'),(35,'Can delete found',9,'delete_found'),(36,'Can view found',9,'view_found'),(37,'Can add lost',10,'add_lost'),(38,'Can change lost',10,'change_lost'),(39,'Can delete lost',10,'delete_lost'),(40,'Can view lost',10,'view_lost'),(41,'Can add student',11,'add_student'),(42,'Can change student',11,'change_student'),(43,'Can delete student',11,'delete_student'),(44,'Can view student',11,'view_student');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$e0qhAM6Mx0S9U4SXFyCT3Z$XdtZZBeIuRrZ4ievz+wOcw13bVr7in9W3nhoWzH7UiE=','2024-11-20 17:15:10.364042',1,'admin1','','','admin1@gmail.com',1,1,'2024-11-12 07:33:38.206000'),(3,'pbkdf2_sha256$870000$RY95TTAH8pVjoKYfVnMW1o$TlpLWrgXLAziJMt6MhXWXCYgaBGlWYAGsEwWenk/NmQ=',NULL,0,'6610625011','','','',0,1,'2024-11-12 10:11:57.470000'),(4,'pbkdf2_sha256$870000$4ab4hfXkd5rGTY0WgVbh0m$0bbtZwh7xKoE5GQiR+M3RCk2whrDsLjlpY37CcuTYfk=',NULL,0,'tu_folksong','','','',0,1,'2024-11-16 16:08:01.315000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-11-12 09:22:36.810000','2','6610625011',1,'[{\"added\": {}}]',4,1),(2,'2024-11-12 10:08:46.018000','2','6610625011',3,'',4,1),(3,'2024-11-12 10:11:57.728000','3','6610625011',1,'[{\"added\": {}}]',4,1),(4,'2024-11-12 10:16:27.878000','1','Chutikarn Keedkum (6610625011)',1,'[{\"added\": {}}]',11,1),(5,'2024-11-12 11:50:32.720000','1','ลอยกระทงธรรมศาสตร์2024 🎆🎡',1,'[{\"added\": {}}]',7,1),(6,'2024-11-16 16:08:01.570000','4','tu_folksong',1,'[{\"added\": {}}]',4,1),(7,'2024-11-16 16:10:16.262000','2','TU Folksong (None)',1,'[{\"added\": {}}]',11,1),(8,'2024-11-18 08:03:09.912000','1','ลอยกระทงธรรมศาสตร์2024 🎆🎡',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1),(9,'2024-11-18 08:43:38.938000','1','ลอยกระทงธรรมศาสตร์2024 🎆🎡',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1),(10,'2024-11-18 08:43:44.233000','1','ลอยกระทงธรรมศาสตร์2024 🎆🎡',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1),(11,'2024-11-18 10:26:39.329000','1','ลอยกระทงธรรมศาสตร์2024',2,'[{\"changed\": {\"fields\": [\"Title\"]}}]',7,1),(12,'2024-11-19 13:26:22.321000','2','เชิญชวนนักชิม',1,'[{\"added\": {}}]',7,1),(13,'2024-11-19 13:26:39.483000','2','เชิญชวนนักชิม',2,'[{\"changed\": {\"fields\": [\"Place\"]}}]',7,1),(14,'2024-11-19 13:28:40.143000','2','เชิญชวนนักชิม',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1),(15,'2024-11-20 12:50:24.335000','3','jujitsu self defense',1,'[{\"added\": {}}]',7,1),(16,'2024-11-20 12:51:26.758000','2','เชิญชวนนักชิม',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1),(17,'2024-11-20 12:51:34.003000','2','เชิญชวนนักชิม',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'web_tu_events','announcement'),(8,'web_tu_events','club'),(9,'web_tu_events','found'),(10,'web_tu_events','lost'),(11,'web_tu_events','student');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-11-20 15:04:02.799827'),(2,'auth','0001_initial','2024-11-20 15:04:03.019578'),(3,'admin','0001_initial','2024-11-20 15:04:03.078914'),(4,'admin','0002_logentry_remove_auto_add','2024-11-20 15:04:03.101209'),(5,'admin','0003_logentry_add_action_flag_choices','2024-11-20 15:04:03.108806'),(6,'contenttypes','0002_remove_content_type_name','2024-11-20 15:04:03.150555'),(7,'auth','0002_alter_permission_name_max_length','2024-11-20 15:04:03.178480'),(8,'auth','0003_alter_user_email_max_length','2024-11-20 15:04:03.197350'),(9,'auth','0004_alter_user_username_opts','2024-11-20 15:04:03.204919'),(10,'auth','0005_alter_user_last_login_null','2024-11-20 15:04:03.243177'),(11,'auth','0006_require_contenttypes_0002','2024-11-20 15:04:03.244074'),(12,'auth','0007_alter_validators_add_error_messages','2024-11-20 15:04:03.252421'),(13,'auth','0008_alter_user_username_max_length','2024-11-20 15:04:03.284891'),(14,'auth','0009_alter_user_last_name_max_length','2024-11-20 15:04:03.313980'),(15,'auth','0010_alter_group_name_max_length','2024-11-20 15:04:03.330328'),(16,'auth','0011_update_proxy_permissions','2024-11-20 15:04:03.339041'),(17,'auth','0012_alter_user_first_name_max_length','2024-11-20 15:04:03.370415'),(18,'sessions','0001_initial','2024-11-20 15:04:03.386650'),(19,'web_tu_events','0001_initial','2024-11-20 15:04:03.422037'),(20,'web_tu_events','0002_student_announcement_place_found_description_and_more','2024-11-20 15:04:03.669121'),(21,'web_tu_events','0003_alter_club_origin','2024-11-20 15:04:03.671258'),(22,'web_tu_events','0004_student_user','2024-11-20 15:04:03.704134'),(23,'web_tu_events','0005_alter_student_image','2024-11-20 15:04:03.731195'),(24,'web_tu_events','0006_alter_student_image','2024-11-20 15:04:03.739807'),(25,'web_tu_events','0007_alter_announcement_date_alter_announcement_end_date_and_more','2024-11-20 15:04:03.764089'),(26,'web_tu_events','0008_club_image_alter_announcement_image_alter_lost_image','2024-11-20 15:04:03.797067'),(27,'web_tu_events','0009_alter_announcement_categories','2024-11-20 15:04:03.799683'),(28,'web_tu_events','0010_alter_announcement_end_date_and_more','2024-11-20 15:04:03.833293'),(29,'web_tu_events','0011_alter_announcement_end_date_and_more','2024-11-20 15:04:03.838467'),(30,'web_tu_events','0012_student_is_active_alter_announcement_end_date_and_more','2024-11-20 15:04:03.889294'),(31,'web_tu_events','0013_remove_student_is_active_alter_student_student_id_and_more','2024-11-20 15:04:03.945138');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('g4rwwcwr0any5hq0wlieljoj8aznsr6v','.eJxVjEEOwiAQRe_C2hCYghSX7j0DGWBGqgaS0q6Md7dNutDtf-_9twi4LiWsneYwZXERWpx-t4jpSXUH-YH13mRqdZmnKHdFHrTLW8v0uh7u30HBXraakzKODFqFDOCtJzsA09krjOxY8zggKBNZg9YmG2JPDmjYrDFiduLzBeggN_0:1tDk6R:OQKSBjBea0wF0usbX7q9WEpU7iSdMQdpB30oOb-SuvM','2024-12-04 12:46:39.145000'),('j2s2t153gdfqi9mzshtzts52qapmc7nj','.eJxVjEEOwiAQRe_C2hCYghSX7j0DGWBGqgaS0q6Md7dNutDtf-_9twi4LiWsneYwZXERWpx-t4jpSXUH-YH13mRqdZmnKHdFHrTLW8v0uh7u30HBXraakzKODFqFDOCtJzsA09krjOxY8zggKBNZg9YmG2JPDmjYrDFiduLzBeggN_0:1tDoII:uVjjTehFiQ6GxjJVHELEsznzxD_UDeNl-YRhVt7XK_o','2024-12-04 17:15:10.370145'),('v2nnyviezpc5rgy8bsvuego12fr2lelu','.eJxVjEEOwiAQRe_C2hCYghSX7j0DGWBGqgaS0q6Md7dNutDtf-_9twi4LiWsneYwZXERWpx-t4jpSXUH-YH13mRqdZmnKHdFHrTLW8v0uh7u30HBXraakzKODFqFDOCtJzsA09krjOxY8zggKBNZg9YmG2JPDmjYrDFiduLzBeggN_0:1tAlQS:zLx47U48okabOV3Si9GVjDiLcaQQWq-zNyu6oQPx7j4','2024-11-26 07:35:00.610000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_tu_events_announcement`
--

DROP TABLE IF EXISTS `web_tu_events_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_tu_events_announcement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `categories` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `place` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_tu_events_announcement`
--

LOCK TABLES `web_tu_events_announcement` WRITE;
/*!40000 ALTER TABLE `web_tu_events_announcement` DISABLE KEYS */;
INSERT INTO `web_tu_events_announcement` VALUES (1,'ลอยกระทงธรรมศาสตร์2024','พร้อมหรือยังกับแสงเรืองรองของจันทราเจิดจ้ายามราตรี 🌠✨\r\n\r\n🕯️ ตำนานอันแสนยิ่งใหญ่แห่งธรรมศาสตร์กำลังจะเริ่มต้นขึ้นอีกครั้งไปกับงาน ลอยกระทงธรรมศาสตร์2024 พร้อมบูธกิจกรรมและวงดนตรีมากมายที่จะคลายความเครียดไปพร้อมกับงานกระทงในปีนี้ 🎧🪗\r\n\r\n🌙 แสงจันทร์ในครั้งนี้จะร่วมเป็นส่วนหนึ่งแห่งสักขีพยานให้คำอธิษฐานของชาวธรรมศาสตร์กลายเป็นจริง โดยผู้ที่อธิษฐานใต้แสงจันทร์จะได้พบเจอกับความสุขและความสนุกอีกมากมายไปกับเราได้ที่งานลอยกระทงธรรมศาสตร์2024 🎆🎡 พาชมวิถีสี่ภาค แสงจันทร์ส่อง สานสุขใจ ไปด้วยกัน\r\n\r\n🎇 มาร่วมเติมเต็มความหวังและความฝันเพื่อสร้างความทรงจำที่ไม่มีวันลืม ไปพร้อมกับแสงจันทร์อันอบอุ่นในคืนแสนพิเศษที่กำลังจะมาถึงนี้ 🔅\r\n\r\n🎈ในวันที่ 14 - 15 พฤศจิกายน 2567 นี้ ณ อาคารโดมบริหาร มหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต!','466130574_1158836435859063_1343952594263775595_n.jpg','2024-11-18 10:26:39.326000','cultural','2024-11-14 12:00:00.000000','2024-11-15 18:00:00.000000','อาคารโดมบริหาร มหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต'),(2,'เชิญชวนนักชิม','📢 นักชิมโปรดเตรียมตัวให้พร้อม❗️✨🍽️\r\nกับการเป็นตัวแทนคัดเลือกร้านค้าฯ พื้นที่ศูนย์อาหารที่ใหญ่ที่สุดของธรรมศาสตร์🔥🔥🔥\r\nมีมากกว่า 140+ ร้าน ที่ผ่านเข้ารอบในการเข้าร่วมคัดเลือกครั้งนี้\r\n\r\n📌เช็คผลทางอีเมล์ของท่านและลงเวลาให้พร้อม!\r\n⏰มาเจอกันวันพรุ่งนี้เวลา 15.00 น. (ควรมาก่อนเวลา 30 นาที)\r\n📍ตลาดนัดอินเตอร์โซน : https://maps.app.goo.gl/JjykvCy5X1CxTF4K9\r\n\r\n#ศูนย์อาหารธรรมศาสตร์ #พื้นที่เช่าธรรมศาสตร์ #นักชิมธรรมศาสตร์','chuanchim.jpg','2024-11-20 12:51:34.002000','entertainment','2024-11-19 18:00:00.000000','2024-11-20 18:00:00.000000','ตลาดนัดอินเตอร์โซน มหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต'),(3,'jujitsu self defense','ใครอยากเท่แบบมีสกิลป้องกันตัวห้ามพลาด!😎\r\nมาสนุกกับ Jujitsu Self-Defense กันในวันที่ 2, 4, 5 กันยายนนี้\r\nเวลา 17.30 - 19.30 น. ไม่ต้องมีพื้นฐานก็เริ่มได้ รับรองสนุกแน่นอน! #JujitsuTU #พร้อมลุย','jujitsuselfdefence.jpg','2024-11-20 12:50:24.333000','sports','2024-09-02 17:30:00.000000','2024-09-05 19:30:00.000000','ลานพญานาค เมนสเตเดียม');
/*!40000 ALTER TABLE `web_tu_events_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_tu_events_club`
--

DROP TABLE IF EXISTS `web_tu_events_club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_tu_events_club` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `enable_to_join` tinyint(1) NOT NULL,
  `origin` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_tu_events_club`
--

LOCK TABLES `web_tu_events_club` WRITE;
/*!40000 ALTER TABLE `web_tu_events_club` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_tu_events_club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_tu_events_found`
--

DROP TABLE IF EXISTS `web_tu_events_found`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_tu_events_found` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `items_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `found_at` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `founded_status` tinyint(1) NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL DEFAULT (_utf8mb3'description'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_tu_events_found`
--

LOCK TABLES `web_tu_events_found` WRITE;
/*!40000 ALTER TABLE `web_tu_events_found` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_tu_events_found` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_tu_events_lost`
--

DROP TABLE IF EXISTS `web_tu_events_lost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_tu_events_lost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `items_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lost_at` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `founded_status` tinyint(1) NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL DEFAULT (_utf8mb3'description'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_tu_events_lost`
--

LOCK TABLES `web_tu_events_lost` WRITE;
/*!40000 ALTER TABLE `web_tu_events_lost` DISABLE KEYS */;
/*!40000 ALTER TABLE `web_tu_events_lost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_tu_events_student`
--

DROP TABLE IF EXISTS `web_tu_events_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_tu_events_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `student_id` bigint DEFAULT NULL,
  `username` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `web_tu_events_student_user_id_981f0518_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_tu_events_student`
--

LOCK TABLES `web_tu_events_student` WRITE;
/*!40000 ALTER TABLE `web_tu_events_student` DISABLE KEYS */;
INSERT INTO `web_tu_events_student` VALUES (1,'','6610685011@dome.tu.ac.th','Chutikarn Keedkum',6610625011,'6610625011','',3),(2,'','tu_folksong@dome.tu.ac.th','TU Folksong',NULL,'tu_folksong','',4);
/*!40000 ALTER TABLE `web_tu_events_student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-21  1:29:20
