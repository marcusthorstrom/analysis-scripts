"""
Created by nuffer at 3/25/20

"""
from analysis.utils.db import IndividualReportModel


class IndividualReportFactory:

    @staticmethod
    def build(json_object):
        seconds = json_object["data"]["timestamp"]["_seconds"]
        nanoseconds = json_object["data"]["timestamp"]["_nanoseconds"]
        timestamp = (seconds + nanoseconds/1000000000) * 1000  # to milliseconds
        symptoms = json_object["data"]["symptoms"]

        return IndividualReportModel(
            document_id=json_object["id"],
            diagnostic=json_object["data"]["diagnostic"],
            locator=json_object["data"]["locator"],
            session_id=json_object["data"]["sessionId"],
            timestamp=timestamp,
            analysis_done=False,
            # FIXME: need to be changed if the website is updated with new
            # questions based on 1177 guidelines
            symptoms=str(symptoms),
            temp="mid" if "fever" in symptoms else "low",
            cough="sometimes" if "cough" in symptoms else "no",
            breathless="sometimes" if "dyspnea" in symptoms else "no",
            energy="tired" if "weakness" in symptoms else "normal"
        )
