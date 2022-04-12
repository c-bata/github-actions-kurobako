FROM python:3.8

RUN pip install PyGithub

COPY entrypoint.sh /entrypoint.sh
COPY report.py /report.py

ENTRYPOINT ["/entrypoint.sh"]
