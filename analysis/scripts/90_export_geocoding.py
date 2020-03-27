"""
Created by nuffer at 3/25/20

"""
import csv
from analysis.utils.db import LocationModel
from analysis.utils.db import session
from analysis import OUTPUT_GEO_CODING_FILE

if __name__ == '__main__':

    fieldnames = [
        'npa_plz',
        'town',
        'state',
        'latitude',
        'longitude'
    ]

    with open(str(OUTPUT_GEO_CODING_FILE), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # query all location first
        q = session.query(LocationModel)
        locations = q.all()
        for location in locations:

            writer.writerow({
                'npa_plz': location.npa,
                'town': location.town,
                'state': location.state,
                'longitude': location.longitude,
                'latitude': location.latitude
            })





