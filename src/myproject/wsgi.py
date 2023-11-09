from os import getenv

from myproject.app import create_app


env = getenv("ENVIRONMENT", "development")
app = create_app(f"myproject.config.{env.capitalize()}")
