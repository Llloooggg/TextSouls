set echo off

export FLASK_APP=textsouls

flask db init
flask db migrate
flask db upgrade