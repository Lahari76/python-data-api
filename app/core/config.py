import os


class Settings:
    DB_NAME = os.getenv("DB_NAME", "python_data_api")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    @property
    def database_url(self):
        if self.DB_PASSWORD:
            credentials = f"{self.DB_USER}:{self.DB_PASSWORD}"
        else:
            credentials = self.DB_USER

        return (
            f"postgresql+psycopg2://{credentials}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
