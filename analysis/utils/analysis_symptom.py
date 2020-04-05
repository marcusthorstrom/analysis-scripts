import time
from datetime import datetime, date

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.exc import InternalError

from analysis.utils.db import engine, session
from analysis.utils.db import DailyDiagnosticChangeModel
from analysis.utils.db import IndividualReportModel
from analysis.utils import db_enum as enum


def calculate(report):
    """Calculate symptom factor per report / row."""
    S = sum(
        column.value
        for column in (
            enum.Scale3[report.temp],
            enum.Scale4[report.cough],
            enum.Scale4[report.breathless],
            enum.Energy[report.energy],
        )
    )
    return S


def map_calculate(collection_size: int):
    """Calcalate symptom factor S for the whole DB where analysis_done = 0"""
    start_time_analysis = time.time()

    # load the next collection of reports to analyse
    next_reports = pd.read_sql(
        (
            "SELECT * FROM individual_report WHERE analysis_done = 0 "
            "ORDER BY timestamp LIMIT "
        )
        + str(collection_size),
        con=engine,
        index_col="document_id",
    )

    S = next_reports.apply(calculate, axis=1)
    query = """
        UPDATE individual_report AS old, temp_table AS new
        SET old.S = new.0, old.analysis_done = 1
        WHERE old.document_id = new.document_id
    """
    with engine.begin() as con:
        S.to_sql(
            "temp_table",
            con,
            if_exists="replace",
            dtype={
                "document_id": sa.String(30),
                "S": sa.Integer,
            }
        )
        try:
            con.execute(query)
        except:
            print("ERROR: while executing query: {}".format(query))
        try:
            con.execute("DROP TABLE temp_table")
        except InternalError:
            print("WARNING: no temp_table to drop")

    session.commit()
    spend_time = time.time() - start_time_analysis
    print('Analysed {} samples in {} s'.format(collection_size, spend_time))


def group_reports_by_location():
    # load all previous reports
    report_done_df = pd.read_sql(
        "SELECT * FROM individual_report WHERE analysis_done = 1",
        con=engine,
        index_col="document_id",
    )
    print(report_done_df)

if __name__ == "__main__":
    map_calculate(10)
    group_reports_by_location()
