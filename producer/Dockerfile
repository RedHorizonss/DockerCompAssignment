FROM python:latest
ADD producer/producer_script.py producer/producer.py konnections.py infofile.py ./
RUN pip install --upgrade pika
CMD ["python", "./producer.py"]