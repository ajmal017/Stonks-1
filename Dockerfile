FROM python:3.8

RUN mkdir /app

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry lxml

RUN poetry config virtualenvs.create false

COPY /yahoo_puts /app

COPY pyproject.toml /app 

RUN poetry install --no-dev

CMD ["streamlit", "run", "/app/yahoo_puts/dashboard.py"]