from analysis.utils.download_report import download_hours_frame


def run_selected_frame():
    from_time = '2020-03-27T12'
    to_time = '2020-03-27T14'
    download_hours_frame(from_time, to_time, 10)


if __name__ == '__main__':
    run_selected_frame()

