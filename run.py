from app import create_app
from instance.db_config import DbSetup

app = create_app('production')

db_setup = DbSetup(app) 

db_setup.create_users_table()
db_setup.create_incidents_table()
db_setup.create_default_admin()

if __name__=='__main__':
    app.run()
    