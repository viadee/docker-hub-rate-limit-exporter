FROM python:3

RUN mkdir /src
COPY ./requirements.txt /src
RUN pip install -r /src/requirements.txt
COPY ./collector.py /src

WORKDIR /src
ENV PYTHONPATH '/src/'

EXPOSE 80/TCP

ENTRYPOINT ["python", "/src/collector.py"]
