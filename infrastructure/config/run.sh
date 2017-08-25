#!/bin/bash

set -o errexit

# wait for postgres
sleep 10
cd /opt

if [ ! -f /reqdbcreated ]; then
  echo "Creating all tables"
  python3 -m reqlog.dbmgt --create_database --config /etc/reqlog/app.conf

  echo "Initializing database with initial data"
  python3 -m reqlog.dbmgt --init_database --config /etc/reqlog/app.conf  
  touch /reqdbcreated
fi

echo "Starting application"
/usr/bin/supervisord
