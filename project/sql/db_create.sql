CREATE DATABASE IF NOT EXISTS social_db
  CHAR SET = utf8
  COLLATE utf8_general_ci;

USE social_db;

DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id         INTEGER      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(64)  NOT NULL,
  last_name  VARCHAR(64)  NOT NULL,
  email      VARCHAR(128) NOT NULL
)
  ENGINE = InnoDB, AUTO_INCREMENT = 1, DEFAULT CHARSET = utf8;

CREATE TABLE comments (
  id        INTEGER      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parent_id INTEGER               DEFAULT NULL,
  user_id   INTEGER      NOT NULL,
  content   VARCHAR(512) NOT NULL,
  pub_date  DATETIME              DEFAULT NULL
)
  ENGINE = InnoDB, AUTO_INCREMENT = 1, DEFAULT CHARSET = utf8;

ALTER TABLE comments
  ADD CONSTRAINT fk_userComments FOREIGN KEY (user_id) REFERENCES users (id)
  ON DELETE CASCADE;


INSERT INTO users (`id`, `first_name`, `last_name`, `email`) VALUES (1, 'John', 'Smith', 'john@mail.com');
INSERT INTO users (`id`, `first_name`, `last_name`, `email`) VALUES (2, 'Kate', 'Anderson', 'kate@mail.com');

INSERT INTO comments (`id`, `parent_id`, `user_id`, `content`, `pub_date`)
VALUES (1, NULL, 1, 'root comment 1', '2016-11-18 11:00:00');
INSERT INTO comments (`id`, `parent_id`, `user_id`, `content`, `pub_date`)
VALUES (2, NULL, 1, 'root comment 2', '2016-11-18 11:05:00');
INSERT INTO comments (`id`, `parent_id`, `user_id`, `content`, `pub_date`)
VALUES (3, NULL, 2, 'root comment 3', '2016-11-18 11:20:00');
INSERT INTO comments (`id`, `parent_id`, `user_id`, `content`, `pub_date`)
VALUES (4, 2, 2, 'nested comment 1', '2016-11-18 11:10:00');
INSERT INTO comments (`id`, `parent_id`, `user_id`, `content`, `pub_date`)
VALUES (5, 4, 1, 'nested comment 1.1', '2016-11-18 11:11:00');