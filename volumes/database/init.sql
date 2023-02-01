CREATE TABLE IF NOT EXISTS `Salts` (
    `UUID` UUID UNIQUE,
    `Salt` TEXT,
    PRIMARY KEY(`UUID`)
);

CREATE TABLE IF NOT EXISTS `Member`(
    `Name` TEXT,
    `Phone` TEXT,
    `Birthday` DATE,
    `CPF` LONGTEXT,
    `HashedPassword` TEXT,
    `Founder` BOOLEAN,
    `UUID` UUID UNIQUE,
    `SaltUUID` UUID,
    PRIMARY KEY(`UUID`),
    FOREIGN KEY(`SaltUUID`) REFERENCES Salts(`UUID`)
);


CREATE TABLE IF NOT EXISTS `Admins`(
    `MemberUUID` UUID UNIQUE,
    FOREIGN KEY (`MemberUUID`) REFERENCES Member(`UUID`)
)