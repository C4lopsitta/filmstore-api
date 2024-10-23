FROM python:3.10.10-alpine
LABEL author="c4lopsitta"
LABEL name="Filmstore"

EXPOSE 4200:4200

WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /api

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4200"]
