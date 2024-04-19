CREATE_SCHEMA = """CREATE SCHEMA IF NOT EXISTS `jobmagnet`;"""

Create_User_Table = """
CREATE TABLE IF NOT EXISTS `jobmagnet`.`User` (
  `UserID` INT NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(120) NOT NULL,
  `usertype` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE (`Email`));
  """
Create_Employer_Table = """
CREATE TABLE IF NOT EXISTS `jobmagnet`.`Employer` (
  `employer_id` INT NOT NULL AUTO_INCREMENT,
  `UserID` INT NOT NULL,
  `company_name` VARCHAR(45) NOT NULL,
  `company_size` INT NOT NULL,
  `industry` VARCHAR(45) NOT NULL,
  `website_url` VARCHAR(255) NOT NULL, 
  PRIMARY KEY (`employer_id`),
  FOREIGN KEY (`UserID`) REFERENCES `jobmagnet`.`User` (`UserID`) 
);
"""
Create_Jobseeker_Table = """
CREATE TABLE IF NOT EXISTS `jobmagnet`.`Jobseeker` (
  `jobseeker_id` INT NOT NULL AUTO_INCREMENT,
  `Location` VARCHAR(45) NOT NULL,
  `Resume_url` VARCHAR(255) NOT NULL,
  `Skills` VARCHAR(255) NOT NULL,
  `Education` VARCHAR(255) NOT NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`jobseeker_id`),
  FOREIGN KEY (`UserID`) REFERENCES `jobmagnet`.`User` (`UserID`) 
);
"""


Create_Application_Table = """
CREATE TABLE IF NOT EXISTS `jobmagnet`.`Application` (
  `application_id` INT NOT NULL AUTO_INCREMENT,
  `jobseeker_id` INT NOT NULL,
  `resume_file` VARCHAR(255) NOT NULL,
  `cover_letter` VARCHAR(255) NOT NULL,
  `application_date` DATE NOT NULL,
  `application_status` VARCHAR(45) NOT NULL,
  `job_id` INT NOT NULL,
  PRIMARY KEY (`application_id`),
  FOREIGN KEY (`jobseeker_id`) REFERENCES `jobmagnet`.`Jobseeker` (`jobseeker_id`),  -- Update schema reference
  FOREIGN KEY (`job_id`) REFERENCES `jobmagnet`.`Job_Posting` (`job_id`)
);
"""


Create_Job_Posting_Table = """
CREATE TABLE IF NOT EXISTS `jobmagnet`.`Job_Posting` (
  `job_id` INT NOT NULL AUTO_INCREMENT,
  `location` VARCHAR(45) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `requirements` VARCHAR(255) NOT NULL,
  `closing_date` DATE NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `employer_id` INT NOT NULL,
  PRIMARY KEY (`job_id`),
  FOREIGN KEY (`employer_id`) REFERENCES `jobmagnet`.`Employer` (`employer_id`)  -- Update schema reference
);
"""


