FROM python:3.8.2

# Not going to change much, do it early
ADD requirements.txt /
ADD setup.py /
RUN pip install -r requirements.txt
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0

# Probably going to change, do it later
COPY . .



CMD ["flask", "run"]