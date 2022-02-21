from pydantic import BaseSettings


class CommonSettings:
    APP_NAME: str = "Sleep Tracker"
    DEBUG_MODE: bool = True


class DatabaseSettings:
    DB_URL: str = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    DB_NAME: str = "SleepTracker"


class ServerSettings:
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class Settings(CommonSettings, DatabaseSettings, ServerSettings):
    pass
