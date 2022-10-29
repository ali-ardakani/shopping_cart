# createapp.py
# This file contains the function that is called from the main file when the
# command "createapp" is used. It creates the app folder with name passed as
# argument. It also creates the urls.py, views.py and models.py files in the
# app folder.


import os
import sys

class CreateApp:
    def __init__(self, app_name):
        self.app_name = app_name

    def create_app(self):
        try:
            os.mkdir(self.app_name)
            os.chdir(self.app_name)
            open("urls.py", "w").close()
            open("views.py", "w").close()
            open("models.py", "w").close()
            print(f"App {self.app_name} created successfully")
        except FileExistsError:
            print(f"App {self.app_name} already exists")
            sys.exit(1)