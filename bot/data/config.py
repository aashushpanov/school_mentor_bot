import os


env_vars = os.environ.copy()

BOT_TOKEN = str(env_vars.get("BOT_TOKEN"))

SCHOOL_NAME = str(env_vars.get("SCHOOL_NAME"))