FROM python:3.7.4-buster

COPY run.sh /
COPY app.py /
COPY enums.py /
COPY band_combinations.py /
COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./run.sh"]