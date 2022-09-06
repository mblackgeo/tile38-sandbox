FROM python:3.8.13-slim-bullseye

RUN pip install geopandas pyle38==0.7.0
COPY ./fill.py /fill.py

RUN python fill.py