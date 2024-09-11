import asyncpg


def get_connection():
    return asyncpg.connect(
        host='localhost',
        port=1212,
        database="database",
        user="postgres",
        password="postgres",
    )


def insert_data_to_project(data):
    connection = get_connection()

    await connection.execute(
        """
        INSERT INTO "project"
        """
    )