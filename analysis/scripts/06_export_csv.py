from datetime import datetime, timedelta
from analysis.utils.db import DailyDiagnosticChangeModel
from analysis.utils.db import LocationModel
from analysis.utils.db import session
from analysis import OUTPUT_DATASETS_PATH
from analysis import DAILY_REPORT_DIR
import csv


DAY_FORMAT = '%Y-%m-%d'


def export_daily_report_to_csv():
    from_day = '2020-03-24' #starting date in database !!!
    to_day = '2020-03-29'

    from_date = datetime.strptime(from_day, DAY_FORMAT)
    to_date = datetime.strptime(to_day, DAY_FORMAT)

    # clean the current output
    for _f in DAILY_REPORT_DIR.glob('*.csv'):
        _f.unlink()

    # query all location first
    q = session.query(LocationModel)
    locations = q.all()
    geo_locations = {}
    for location in locations:
        geo_locations[str(location.npa)] = {
            'longitude': location.longitude,
            'latitude': location.latitude,
            'state': location.state
        }

    fieldnames = [
        'date',
        'state',
        'npa_plz',
        'latitude',
        'longitude',
        'total_healthy',
        'total_sick_guess_no_corona',
        'total_sick_guess_corona',
        'total_sick_corona_confirmed',
        'total_recovered_confirmed',
        'total_recovered_not_confirmed',
    ]

    merge_file = OUTPUT_DATASETS_PATH / 'merge-all-days.csv'
    with open(str(merge_file), 'w', newline='') as csvfile:
        merge_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        merge_writer.writeheader()

        # iterate over days
        totals = {}
        current_day = from_date
        while current_day <= to_date:

            # create daily file
            daily_file = DAILY_REPORT_DIR / ('ch-covid-19-' + current_day.strftime(DAY_FORMAT) + '.csv')
            with open(str(daily_file), 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                q = session.query(DailyDiagnosticChangeModel)
                daily_changes = q.filter_by(year=current_day.year, month=current_day.month, day=current_day.day).all()

                print(current_day)
                if daily_changes is not None:
                    for daily_change in daily_changes:
                        try:
                            if daily_change.locator not in totals:
                                # then create it
                                totals[daily_change.locator] = {
                                    'longitude': geo_locations[daily_change.locator]['longitude'],
                                    'latitude': geo_locations[daily_change.locator]['latitude'],
                                    'state': geo_locations[daily_change.locator]['state'],
                                    'data': [
                                        daily_change.diagnostic_0,
                                        daily_change.diagnostic_1,
                                        daily_change.diagnostic_2,
                                        daily_change.diagnostic_3,
                                        daily_change.diagnostic_4,
                                        daily_change.diagnostic_5,
                                    ]
                                }
                            else:
                                # use the previous total
                                totals[daily_change.locator]['data'] = [
                                    totals[daily_change.locator]['data'][0] + daily_change.diagnostic_0,
                                    totals[daily_change.locator]['data'][1] + daily_change.diagnostic_1,
                                    totals[daily_change.locator]['data'][2] + daily_change.diagnostic_2,
                                    totals[daily_change.locator]['data'][3] + daily_change.diagnostic_3,
                                    totals[daily_change.locator]['data'][4] + daily_change.diagnostic_4,
                                    totals[daily_change.locator]['data'][5] + daily_change.diagnostic_5,
                                ]

                            # totals cannot be negative, just fix if some errors are present in the dataset
                            if totals[daily_change.locator]['data'][0] < 0:
                                totals[daily_change.locator]['data'][0] = 0
                            if totals[daily_change.locator]['data'][1] < 0:
                                totals[daily_change.locator]['data'][1] = 0
                            if totals[daily_change.locator]['data'][2] < 0:
                                totals[daily_change.locator]['data'][2] = 0
                            if totals[daily_change.locator]['data'][3] < 0:
                                totals[daily_change.locator]['data'][3] = 0
                            if totals[daily_change.locator]['data'][4] < 0:
                                totals[daily_change.locator]['data'][4] = 0
                            if totals[daily_change.locator]['data'][5] < 0:
                                totals[daily_change.locator]['data'][5] = 0


                        except KeyError:
                            # wrong npa
                            print('Wrong npa: ' + daily_change.locator)

                total_status = 0
                # export all totals in the current day
                # this take into account the total from previous days if no daily change in the current day
                for npa, total in totals.items():
                    total_status += sum(total['data'])
                    writer.writerow({
                        'npa_plz': npa,
                        'state': total['state'],
                        'longitude': total['longitude'],
                        'latitude': total['latitude'],
                        'date': current_day.strftime(DAY_FORMAT),
                        'total_healthy': total['data'][0],
                        'total_sick_guess_no_corona': total['data'][1],
                        'total_sick_guess_corona': total['data'][2],
                        'total_sick_corona_confirmed': total['data'][3],
                        'total_recovered_not_confirmed': total['data'][4],
                        'total_recovered_confirmed': total['data'][5],
                    })
                    merge_writer.writerow({
                        'npa_plz': npa,
                        'state': total['state'],
                        'longitude': total['longitude'],
                        'latitude': total['latitude'],
                        'date': current_day.strftime(DAY_FORMAT),
                        'total_healthy': total['data'][0],
                        'total_sick_guess_no_corona': total['data'][1],
                        'total_sick_guess_corona': total['data'][2],
                        'total_sick_corona_confirmed': total['data'][3],
                        'total_recovered_not_confirmed': total['data'][4],
                        'total_recovered_confirmed': total['data'][5],
                    })
                print(total_status)

            current_day = current_day + timedelta(days=1)


if __name__ == '__main__':
    export_daily_report_to_csv()

