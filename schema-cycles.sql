CREATE TABLE `cycles` (
        `epochtime`     REAL(64),
        `cycletime`     timestamp,
        `dt`    REAL(64),
        `speed_mph`     REAL(64),
        `distance` REAL(64),
        PRIMARY KEY(`epochtime`)
);
