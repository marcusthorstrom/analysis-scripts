import csv
from analysis import GEO_DATA_FILE_FIRST
from analysis import GEO_DATA_FILE_SECOND
from analysis.utils.db import LocationModel
from analysis.utils.db import session


def upload_geo_data():

    geo_locations = {}
    with open(str(GEO_DATA_FILE_FIRST), 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header

            location = {
                'npa': int(row[5]),
                'town': row[4],
                'state': row[3],
                'longitude': float(row[2]),
                'latitude': float(row[1]),
            }

            # remove duplicate by this...
            geo_locations[location['npa']] = location

    with open(str(GEO_DATA_FILE_SECOND), 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header

            location = {
                'npa': int(row[0]),
                'town': row[1],
                'state': row[2],
                'longitude': float(row[3]),
                'latitude': float(row[4]),
            }

            if location['npa'] in geo_locations:
                geo_locations[location['npa'] ]['town'] = location['town']
                geo_locations[location['npa'] ]['longitude'] = location['longitude']
                geo_locations[location['npa'] ]['latitude'] = location['latitude']
            else:
                # add it
                geo_locations[location['npa']] = location

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
