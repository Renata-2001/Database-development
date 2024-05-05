-- MySQL Script generated by MySQL Workbench
-- Sun May  5 13:49:05 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema APPLICATION
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema APPLICATION
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `APPLICATION` DEFAULT CHARACTER SET utf8 ;
USE `APPLICATION` ;

-- -----------------------------------------------------
-- Table `APPLICATION`.`clients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`clients` (
  `name` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `numberphone` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NULL,
  `id_client` INT NOT NULL AUTO_INCREMENT,
  UNIQUE INDEX `numberphone_UNIQUE` (`numberphone` ASC) VISIBLE,
  PRIMARY KEY (`id_client`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `APPLICATION`.`master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`master` (
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `id_master` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  PRIMARY KEY (`id_master`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `APPLICATION`.`services`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`services` (
  `id_service` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `time_spent` INT NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_service`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `APPLICATION`.`records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`records` (
  `id_record` INT NOT NULL AUTO_INCREMENT,
  `id_clients` INT NOT NULL,
  `id_services` INT NOT NULL,
  `id_masters` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_record`),
  INDEX `id_client_idx` (`id_clients` ASC) VISIBLE,
  INDEX `id_services_idx` (`id_services` ASC) VISIBLE,
  INDEX `id_master_idx` (`id_masters` ASC) VISIBLE,
  CONSTRAINT `id_clients`
    FOREIGN KEY (`id_clients`)
    REFERENCES `APPLICATION`.`clients` (`id_client`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_services`
    FOREIGN KEY (`id_services`)
    REFERENCES `APPLICATION`.`services` (`id_service`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_masters`
    FOREIGN KEY (`id_masters`)
    REFERENCES `APPLICATION`.`master` (`id_master`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `APPLICATION`.`skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`skills` (
  `service_id` INT NOT NULL,
  `master_id` INT NOT NULL,
  PRIMARY KEY (`service_id`, `master_id`),
  INDEX `id_master_idx` (`master_id` ASC) VISIBLE,
  CONSTRAINT `services_id`
    FOREIGN KEY (`service_id`)
    REFERENCES `APPLICATION`.`services` (`id_service`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `master_id`
    FOREIGN KEY (`master_id`)
    REFERENCES `APPLICATION`.`master` (`id_master`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `APPLICATION`.`SCHEDULE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `APPLICATION`.`SCHEDULE` (
  `id_SCHEDULE` INT NOT NULL AUTO_INCREMENT,
  `id_masters` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  PRIMARY KEY (`id_SCHEDULE`),
  INDEX `id_master_idx` (`id_masters` ASC) VISIBLE,
  CONSTRAINT `id_master`
    FOREIGN KEY (`id_masters`)
    REFERENCES `APPLICATION`.`master` (`id_master`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
