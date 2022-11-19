import json

import sqlalchemy
from sqlalchemy.orm import Session

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

engine = sqlalchemy.create_engine(
    config_data["DB_SETTINGS"]["SQLALCHEMY_DATABASE_URI"]
)
metadata = sqlalchemy.MetaData(bind=engine)

with open("scripts/init_data.json") as seed_file:
    seed_data = json.load(seed_file)

for table_data in seed_data:
    table = sqlalchemy.Table(table_data["table_name"], metadata, autoload=True)

    query = table.insert().values(table_data["records"])

    session = Session(engine)
    session.execute(query)
    session.commit()
    session.close()
