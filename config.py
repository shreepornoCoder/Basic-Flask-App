import os

class Config:
    SECRET_KEY = "myownsecretkey"
    project_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(project_dir, 'data', 'db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
