import csv
from analysis import GEO_DATA_FILE_FIRST
from analysis import TMP_PATH
from analysis import GEO_DATA_FILE_SECOND
from analysis.utils.db import LocationModel
from analysis.utils.db import session
import requests


GEOCODING_RAW_FILE_URL = "https://raw.githubusercontent.com/ch-covid-19/geo-locations/master/data/mex/MEX_geocoding.csv"

GEOCODING_RAW_FILE = TMP_PATH / 'geocoding.csv'


def download_geocoding_file():
    print("downloading geocoding file...")
    response = requests.get(GEOCODING_RAW_FILE_URL)
    data = response.text
    f = open(str(GEOCODING_RAW_FILE), "w")
    f.write(data)
    f.close()
    print("downloading geocoding file: done")


def upload_geo_data():

    geo_locations = {}
    with open(str(GEOCODING_RAW_FILE), 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header

            print(row)

            return
            location = {
                'country_code': int(row[5]),
                'town': row[4],
                'state': row[3],
                'longitude': float(row[2]),
                'latitude': float(row[1]),
            }

            # remove duplicate by this...
            geo_locations[location['npa']] = location

            print(geo_locations)
            return


    for key, loc in geo_locations.items():
        location = LocationModel(
            npa=loc['npa'],
            town=loc['town'],
            state=loc['state'],
            longitude=loc['longitude'],
            latitude=loc['latitude'],
        )
        session.add(location)
    session.commit()


if __name__ == '__main__':
    upload_geo_data()
