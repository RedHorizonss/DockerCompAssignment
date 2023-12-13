FROM python:latest
ADD outputter/outputter_script.py outputter/outputter.py konnections.py infofile.py ./
RUN pip install --upgrade pika awkward numpy matplotlib
CMD ["python", "./outputter.py"]