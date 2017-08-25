#!/bin/bash

set -o errexit

# wait for postgres
sleep 10
cd {working_directory}

if [ ! -f /{application}_db_created ]; then
  echo "Creating all tables"
  python3 -m {dbmgt_script} --create_database --config /etc/{application}/app.conf

  echo "Initializing database with initial data"
  python3 -m {dbmgt_script} --init_database --config /etc/{application}/app.conf  
  touch /{application}_db_created
fi

echo "Starting application"
/usr/bin/supervisord
