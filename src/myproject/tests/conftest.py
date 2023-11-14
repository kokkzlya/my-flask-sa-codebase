import os

pytest_plugins = [
    "fixtures.app"
]

os.environ["ENVIRONMENT"] = "testing"
