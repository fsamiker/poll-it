from backend.api.models import Option, Poll, User, Vote
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from backend.api import create_app, db


app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.shell
def shell_ctx():
    return dict(app=app,
            db=db,
            User=User,
            Poll=Poll,
            Option=Option,
            Vote=Vote)

if __name__ == '__main__':
    manager.run()