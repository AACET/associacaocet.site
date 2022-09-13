import os
import sqlite3
from types import FunctionType
from typing import Any
from . import config
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
