# manage.py
# This file contains the function that is managed commands from the main file.

import os
import uvicorn
from config import settings
import sys
import pytest

class Manage:

    @staticmethod
    def manage():
        command = sys.argv[1]
        if command == "createapp":
            try:
                app_name = sys.argv[2]
                CreateApp.create_app(app_name)
            except IndexError:
                print("Please provide an app name")
                sys.exit(1)
        elif command == "runserver":
            RunServer.run_server()
        elif command == "test":
            Test.test()
        else:
            print("Command not found")
            sys.exit(1)


class RunServer:
    @staticmethod
    def run_server():
        if len(sys.argv) > 2:
            parm = sys.argv[2].split(":")
            host = "".join(parm[:-1])
            port = int(parm[-1])
        else:
            host = settings.HOST
            port = settings.PORT
        uvicorn.run("main:app", host=host, port=port, reload=True)

class CreateApp:

    @staticmethod
    def create_app(app_name):
        try:
            os.mkdir(app_name)
            os.chdir(app_name)
            open("urls.py", "w").close()
            open("views.py", "w").close()
            open("models.py", "w").close()
            print(f"App {app_name} created successfully")
        except FileExistsError:
            print(f"App {app_name} already exists")
            sys.exit(1)

class Test:
    
    @staticmethod
    def test():
        try:
            app_name = sys.argv[2]
            if app_name in settings.INSTALLED_APPS:
                pytest.main([app_name + "/tests.py"])
            else:
                print(f"App {app_name} not found")
                sys.exit(1)
        except IndexError:
            test_file = [app_name + "/tests.py" for app_name in settings.INSTALLED_APPS]
            pytest.main([*test_file])
            
        
        os.remove("sql_test.db")
        
