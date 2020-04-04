from analysis.utils.db import engine, session
from sqlalchemy.exc import InternalError

if __name__ == "__main__":
    for table in ("comorbidities", "individual_report", "temp_table"):
        with engine.begin() as con:
            try:
                con.execute("DROP TABLE {}".format(table))
            except InternalError:
                print("WARNING: no temp_table to drop")