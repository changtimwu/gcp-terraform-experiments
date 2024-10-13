FROM python:3.11.3
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV APP_HOME /root/
WORKDIR $APP_HOME
COPY main.py $APP_HOME
COPY static $APP_HOME/static

EXPOSE 8080
CMD ["python", "main.py"]
