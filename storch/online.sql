CREATE TABLE `frames` (
  `idframes` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `thumbnail` blob NOT NULL,
  `fullsizerequested` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`idframes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fullframes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `frameid` int(11) NOT NULL,
  `data` mediumblob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `frame_id` (`frameid`),
  CONSTRAINT `frame_id` FOREIGN KEY (`frameid`) REFERENCES `frames` (`idframes`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `temperature` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `vidrequests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requestID` int(11) NOT NULL,
  `path` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `request_id` (`requestID`),
  CONSTRAINT `request_id` FOREIGN KEY (`requestID`) REFERENCES `vidrequests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

