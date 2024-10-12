-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DB_Almacen
-- -----------------------------------------------------
-- Base de datos para Almacen

-- -----------------------------------------------------
-- Schema DB_Almacen
--
-- Base de datos para Almacen
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DB_Almacen` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `DB_Almacen` ;

-- -----------------------------------------------------
-- Table `DB_Almacen`.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Almacen`.`Categoria` (
  `categoriaID` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(20) NOT NULL,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`categoriaID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DB_Almacen`.`Producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Almacen`.`Producto` (
  `productoID` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(30) NOT NULL,
  `precio` DECIMAL(2) NOT NULL,
  `stock` INT NOT NULL,
  `costo` DECIMAL(2) NOT NULL,
  `codigo_barra` VARCHAR(13) NULL,
  `producto_categoria` INT NOT NULL,
  PRIMARY KEY (`productoID`),
  INDEX `fk_Producto_Categoria_idx` (`producto_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_Categoria`
    FOREIGN KEY (`producto_categoria`)
    REFERENCES `DB_Almacen`.`Categoria` (`categoriaID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DB_Almacen`.`Vendedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Almacen`.`Vendedor` (
  `vendedorID` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(10) NOT NULL,
  `contraseña` INT(4) NOT NULL,
  PRIMARY KEY (`vendedorID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DB_Almacen`.`Venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Almacen`.`Venta` (
  `ventaID` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `total_ventas` DECIMAL(2) NOT NULL,
  `Vendedor_vendedorID` INT NOT NULL,
  PRIMARY KEY (`ventaID`, `Vendedor_vendedorID`),
  INDEX `fk_Venta_Vendedor1_idx` (`Vendedor_vendedorID` ASC) VISIBLE,
  CONSTRAINT `fk_Venta_Vendedor1`
    FOREIGN KEY (`Vendedor_vendedorID`)
    REFERENCES `DB_Almacen`.`Vendedor` (`vendedorID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DB_Almacen`.`Detalle`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Almacen`.`Detalle` (
  `Producto_productoID` INT NOT NULL,
  `Venta_ventaID` INT NOT NULL,
  `cantidad` INT NOT NULL,
  `total_prod` DECIMAL(2) NOT NULL,
  PRIMARY KEY (`Producto_productoID`, `Venta_ventaID`),
  INDEX `fk_Producto_has_Venta_Venta1_idx` (`Venta_ventaID` ASC) VISIBLE,
  INDEX `fk_Producto_has_Venta_Producto1_idx` (`Producto_productoID` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_has_Venta_Producto1`
    FOREIGN KEY (`Producto_productoID`)
    REFERENCES `DB_Almacen`.`Producto` (`productoID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Producto_has_Venta_Venta1`
    FOREIGN KEY (`Venta_ventaID`)
    REFERENCES `DB_Almacen`.`Venta` (`ventaID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
