# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from flask_app import app
from flask_script import Manager


manager = Manager(app)

if __name__ == '__main__':
    manager.run()