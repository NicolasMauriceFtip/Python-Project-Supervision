# Python-Project-Supervision

## TODO before using !

Install psutil
Install mariadb
Install MySQL connector (if needed)

Run the database_create.sql file in pycharm in order to create the appropriate database.
Do not forget to adapt the database connection in function write_to_db on line 175 of supervision.py

Use the Setup Grafana json file to import into Grafana : http://localhost:3000/?orgId=1

## Project Features

### Gathering data using psutil
We use pustil to collect data, of which there are 4 types :
  - Disk usage
  - Memory Usage
  - CPU Usage
  - Net IO counters

### Write collected data to texfile
We export the collected data and organize it towards a readable textfile

### Write into a mariadb database using MySQL connector
We've created tables in order to gather this data into a relational database

### Use the mariadb data to export to grafana and transform the data into information
Grafana allows us to export and transform our data see below for snapshot examples or, if you've configured the project, use the Setup Grafana file to import the configuration to your own Grafana after you've collected data

#### Snapshot examples :
https://snapshot.raintank.io/dashboard/snapshot/45NvcaQPi2UiCP9GVqLa4MakC7zUI5ey?orgId=2

https://snapshot.raintank.io/dashboard/snapshot/vz86ZHB3Q6bvIsu6PnoY0pEWmIvQRw84?orgId=2
