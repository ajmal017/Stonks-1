FROM python:3.8
RUN mkdir /app
COPY /yahoo_puts /app
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry lxml
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD ["streamlit", "run", "/app/yahoo_puts/dashboard.py"]