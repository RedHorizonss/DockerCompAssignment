FROM python:latest
ADD worker/worker.py worker/worker_script.py konnections.py infofile.py ./
RUN pip install --upgrade pika uproot awkward vector
CMD ["python", "./worker.py"]