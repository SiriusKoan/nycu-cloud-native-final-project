FROM python:3.6.15-slim
COPY . /crawler
WORKDIR /crawler
RUN pip install -r ./requirements.txt
CMD ["python", "crawler.py"]
