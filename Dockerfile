FROM python:3
WORKDIR /circle_ci_python_example
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
