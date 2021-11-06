
from simple_forum import create_app
from simple_forum.models import *
from simple_forum.db import db


app = create_app()
app.app_context().push()

