CREATE DATABASE  IF NOT EXISTS `db_almacen` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_almacen`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: db_almacen
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `categoriaID` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) COLLATE utf8mb3_bin NOT NULL,
  `descripcion` varchar(45) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`categoriaID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Bebidas',NULL);
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle`
--

DROP TABLE IF EXISTS `detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle` (
  `Producto_productoID` int NOT NULL,
  `Venta_ventaID` int NOT NULL,
  `cantidad` int NOT NULL,
  `total_prod` decimal(8,2) NOT NULL,
  PRIMARY KEY (`Producto_productoID`,`Venta_ventaID`),
  KEY `fk_Producto_has_Venta_Venta1_idx` (`Venta_ventaID`),
  KEY `fk_Producto_has_Venta_Producto1_idx` (`Producto_productoID`),
  CONSTRAINT `fk_Producto_has_Venta_Producto1` FOREIGN KEY (`Producto_productoID`) REFERENCES `producto` (`productoID`),
  CONSTRAINT `fk_Producto_has_Venta_Venta1` FOREIGN KEY (`Venta_ventaID`) REFERENCES `venta` (`ventaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle`
--

LOCK TABLES `detalle` WRITE;
/*!40000 ALTER TABLE `detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `productoID` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) COLLATE utf8mb3_bin NOT NULL,
  `precio` decimal(8,2) NOT NULL,
  `stock` int NOT NULL,
  `costo` decimal(8,2) NOT NULL,
  `codigo_barra` varchar(13) COLLATE utf8mb3_bin DEFAULT NULL,
  `producto_categoria` int NOT NULL,
  PRIMARY KEY (`productoID`),
  KEY `fk_Producto_Categoria_idx` (`producto_categoria`),
  CONSTRAINT `fk_Producto_Categoria` FOREIGN KEY (`producto_categoria`) REFERENCES `categoria` (`categoriaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendedor`
--

DROP TABLE IF EXISTS `vendedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendedor` (
  `vendedorID` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(10) COLLATE utf8mb3_bin NOT NULL,
  `contrasena` int NOT NULL,
  PRIMARY KEY (`vendedorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendedor`
--

LOCK TABLES `vendedor` WRITE;
/*!40000 ALTER TABLE `vendedor` DISABLE KEYS */;
INSERT INTO `vendedor` VALUES (2,'Leo',1234),(4,'Victor',1234);
/*!40000 ALTER TABLE `vendedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `ventaID` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `total_ventas` decimal(8,2) NOT NULL,
  `Vendedor_vendedorID` int NOT NULL,
  PRIMARY KEY (`ventaID`,`Vendedor_vendedorID`),
  KEY `fk_Venta_Vendedor1_idx` (`Vendedor_vendedorID`),
  CONSTRAINT `fk_Venta_Vendedor1` FOREIGN KEY (`Vendedor_vendedorID`) REFERENCES `vendedor` (`vendedorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'db_almacen'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-15 16:01:55
