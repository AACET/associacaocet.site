from python:bullseye

COPY . /api/.
RUN pip3 install -r /api/requirements.txt

CMD cd /api/ && flask run --port=80 --host=0.0.0.0