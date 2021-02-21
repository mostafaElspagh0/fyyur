import os


class DatabaseUri:
    database_name = "fyyur_dev"
    database_type = 'postgres'
    username = os.getenv('DATABASE_PASSWORD')
    password = os.getenv('DATABASE_PASSWORD')
    if username is None:
        username = 'postgres'
    if password is None:
        password = ''
    server = 'localhost'
    port = 5432

    def __str__(self):
        return f'{self.database_type}://{self.username}:{self.password}@' \
               f'{self.server}:{self.port}/{self.database_name}'
