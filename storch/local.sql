CREATE TABLE `config` (
  `confkey` varchar(64) NOT NULL,
  `confvalue` varchar(256) NOT NULL,
  PRIMARY KEY (`confkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pictures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thumb` blob NOT NULL,
  `full` mediumblob NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
