CREATE TABLE `config` (
  `confkey` varchar(64) NOT NULL,
  `confvalue` varchar(256) NOT NULL,
  PRIMARY KEY (`confkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pictures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full` mediumblob NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `thumbs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thumb` blob NOT NULL,
  `pictureid` int(11) NOT NULL,
  `online` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `thumb_to_pic` (`pictureid`),
  CONSTRAINT `thumb_to_pic` FOREIGN KEY (`pictureid`) REFERENCES `pictures` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
