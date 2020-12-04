FROM python:3-alpine as build

WORKDIR /install

COPY ./requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3-alpine

WORKDIR /src
ENV PYTHONPATH '/src/'

COPY --from=build /install /usr/local
COPY ./collector.py /src

EXPOSE 80/tcp

ENTRYPOINT ["python", "/src/collector.py"]
