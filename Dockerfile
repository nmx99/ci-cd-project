FROM python:3
WORKDIR /circle_ci_python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
