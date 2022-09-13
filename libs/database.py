import os
import sqlite3
from types import FunctionType
from typing import Any
from . import config

tables: dict[str, list[str]] = {
    "users.sql": [
        """
        CREATE TABLE `Courses`(
            `Name` TEXT,
            `UUID` UUID,
            PRIMARY KEY(UUID)  
        )
        """,
        """
        CREATE TABLE `Salts`(
            `UUID` UUID,
            `Hash` TEXT,
            PRIMARY KEY(UUID)
        )
        """,
        """
        CREATE TABLE `Associated`(
            `UUID` UUID,
            `Username` TEXT,
            `FirstName` TEXT,
            `LastName` TEXT,
            `Birthday` DATE,
            `Email` TEXT,
            `UPF_ID` TEXT,
            `PhoneNumber` TEXT,
            `CourseUUID` UUID,
            `Password` TEXT,
            `SaltUUID` UUID,
            `Password_OTP` TOTP,
            `Verification_OTP` TOTP,
            `Active` BOOLEAN,
            PRIMARY KEY(UUID),
            FOREIGN KEY(SaltUUID)
                REFERENCES Salts(UUID),
            FOREIGN KEY(CourseUUID)
                REFERENCES Courses(UUID)
        )
        """,
    ],
    "mail.sql": [
    """
    CREATE TABLE `Pool`(
        `From` TEXT,
        `To` TEXT,
        `MessageID` TEXT,
        `Subject` TEXT,
        `Date` DATETIME,
        `Data` LONGTEXT,      
    )
    """,
    ],
    "event_horizon.sql": []
}


class DatabaseWrapper:
    def __init__(self, function: FunctionType, databases: list[str]):
        self.function = function
        self.databases = databases

    def get_database(self) -> list[sqlite3.Connection|sqlite3.Cursor]:
        connections: list[sqlite3.Connection|sqlite3.Cursor] = []
        for db in self.databases:
            connection = sqlite3.connect(
                os.path.join(config.database.get('base_path'), db)
            )
            connection.execute("PRAGMA foreign_keys = ON")
            connections.append(connection)
            connections.append(connection.cursor())
        return connections
    
    def __call__(self, *args, **kwargs) -> Any:
        connection = self.get_database()
        output = self.function(*connection, *args, **kwargs)
        connection.commit()
        connection.close()


def database_query(*databases):
    return lambda function: DatabaseWrapper(function, databases)
