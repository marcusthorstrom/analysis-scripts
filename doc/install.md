# Install

For installing the analysis scripts

## Install python
We recomand that you activate a virtual environment before.

```bash
sh python_install.sh
```

If you run from analysis-script folder, you might want to set up the PYTHONPATH as below:
`export PYTHONPATH=$PWD/analysis:$PYTHONPATH`

## Install docker
```bash
sh docker_install.sh
```

## Update .env file

yeah...you have to update it.

```bash
# firebase vars
READ_API_URL='https://your_project.cloudfunctions.net/export_json'
READ_TOKEN=''

#docker containers
MYSQL_PORT=3306
PHPMYADMIN_PORT=9000
DOCKER_COVID_MYSQL="docker.covid.mysql"
DOCKER_COVID_ADMIN="docker.covid.phpmyadmin"

# point to your dataset repo
PUBLIC_DATASETS_REPO_RELATIVE_PATH='../datasets'

# other vars
DATABASE_NAME=covid_dev

# your country geocoding file 
GEOCODING_RAW_FILE_URL = "https://raw.githubusercontent.com/ch-covid-19/geo-locations/master/data/mex/MEX_geocoding.csv"
```

## Run docker

Warning, this script is also killing the container berfore restart. So you need to do it once.
```bash
sh docker_run.sh
```

## Create the database

1. Connect to phpmyadmin (http://localhost:9000/db_structure.php)
2. You have to create a database (default: covid_dev) with the same name as in the .env file.
