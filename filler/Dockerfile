FROM python:3.8.13-slim-bullseye

RUN pip install geopandas==0.10.2 pyle38==0.7.0
COPY ./fill.py /fill.py

CMD [ "python", "fill.py" ]