# main.py
# This is the main file for the project. It contains the main loop and the
# functions that are called from the main loop. It also contains the
# functions that are called from the other files.

import fastapi
from commands import Manage
from config.settings import INSTALLED_APPS, Base, engine

description = """
Simple shopping cart application built with FastAPI.
"""

app = fastapi.FastAPI(
    title="Shopping Cart", description=description, version="0.0.1",
    contact={
        "name": "Ali Kamali Ardakani",
        "email": "aliardakani78@gmail.com",
    },
)

for app_name in INSTALLED_APPS:
    app.include_router(
        __import__(app_name + ".urls").urls.router
    )
    
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    Manage.manage()
    