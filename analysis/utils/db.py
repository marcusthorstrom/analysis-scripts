from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from analysis import DATABASE, MYSQL_PORT
from analysis.utils import enum


base = declarative_base()
engine = sa.create_engine('mysql+pymysql://root:root@localhost:' + MYSQL_PORT + '/' + DATABASE)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)


class IndividualReportModel(base):
    """JSON data is translated into SQL table columns."""
    __tablename__ = 'individual_report'
    document_id = sa.Column(sa.String(30), primary_key=True)
    diagnostic = sa.Column(sa.Integer,nullable=False)
    locator = sa.Column(sa.String(15),nullable=False)
    session_id = sa.Column(sa.String(50),nullable=False)
    timestamp = sa.Column(sa.BigInteger, nullable=False)
    # symptoms = sa.Column(sa.String(255))
    analysis_done = sa.Column(sa.Boolean,nullable=False)
    # covidmap specific 
    # old questionnare - incomplete
    # *****************************
    # 1. Basic information
    # --------------------
    # age = sa.Column(sa.Integer, nullable=False)
    # gender = sa.Column(sa.Enum(Gender), nullable=False)
    # pregnant = sa.Column(sa.Boolean)
    # weight = sa.Column(sa.Integer, nullable=False)
    # height = sa.Column(sa.Integer, nullable=False)

    # 2. Epidemological information
    # -----------------------------
    # epi_travel = sa.Column(sa.Boolean, nullable=False)
    # # contact with a confirmed
    # epi_contact = sa.Column(sa.Boolean, nullable=False)

    # 3. Symptoms
    # -----------
    # # chest pain
    # sym_chest =  
    
    # 1177 questions
    # **************
    # Key symptoms
    # ------------
    temp = sa.Column(sa.Enum(enum.Scale3), nullable=False)
    cough = sa.Column(sa.Enum(enum.Scale4), nullable=False)
    breathless = sa.Column(sa.Enum(enum.Scale4), nullable=False)
    energy = sa.Column(sa.Enum(enum.Energy), nullable=False)
    # # If not currently sick (ie NO Q1-4) , provide assessment about risk of
    # # becoming sick
    exposure = sa.Column(sa.Enum(enum.Exposure))
    has_comorbid = sa.Column(sa.Boolean)
    # comorbid = orm.relationship("Comorbid")
    compromised_immune = sa.Column(sa.Boolean)
    age = sa.Column(sa.Enum(enum.Scale3))
    

    def __repr__(self):
        return '<Indiv. report: NPA ' + self.locator + ' time ' + str(self.timestamp) + '>'


# class Comorbid(base):
#     """Do you have any of the following ongoing illnesses? (multiple choice)
    
#     One-to-one mapping
#     ref: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-one
#     """
#     __tablename__ = "comorbidities"
#     parent_id = sa.Column(
#         sa.String(30),
#         sa.ForeignKey('individual_report.document_id')
#     )
#     hypertension = sa.Column(sa.Boolean)
#     cardiovascular = sa.Column(sa.Boolean)
#     pulmonary = sa.Column(sa.Boolean)
#     cancer = sa.Column(sa.Boolean)
#     diabetes = sa.Column(sa.Boolean)
#     renal = sa.Column(sa.Boolean)
#     neurological = sa.Column(sa.Boolean)
#     respiratory = sa.Column(sa.Boolean)


class DailyDiagnosticChangeModel(base):
    __tablename__ = 'daily_diagnostic_change'
    id = sa.Column(sa.Integer, primary_key=True,autoincrement=True)
    locator = sa.Column(sa.String(15))
    date = sa.Column(sa.Date)
    diagnostic_0 = sa.Column(sa.Integer, default=0)
    diagnostic_1 = sa.Column(sa.Integer, default=0)
    diagnostic_2 = sa.Column(sa.Integer, default=0)
    diagnostic_3 = sa.Column(sa.Integer, default=0)
    diagnostic_4 = sa.Column(sa.Integer, default=0)
    diagnostic_5 = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        d = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
        change = [
            self.diagnostic_0,
            self.diagnostic_1,
            self.diagnostic_2,
            self.diagnostic_3,
            self.diagnostic_4,
        ]
        return '<DailyChang: NPA ' + self.locator + ' ' + d + ' ' + str(change) + '>'


class LocationModel(base):
    """
    headers from csv: country_code,postal_code,town,region,latitude,longitude
    """
    __tablename__ = 'locations'
    postal_code = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    country_code = sa.Column(sa.String(3))
    region_id = sa.Column(sa.Text)
    longitude = sa.Column(sa.Float)
    latitude = sa.Column(sa.Float)

    def __repr__(self):
        return '<Location: ' + self.postal_code + '>'


def init_db():
    base.metadata.create_all()


