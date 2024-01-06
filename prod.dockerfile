FROM python:3.10

RUN apt-get update && apt-get install -y locales \
    locales-all \
    wkhtmltopdf \
    python3-lxml
RUN locale-gen nl_NL.UTF-8  
ENV LANG nl_NL.UTF-8  
ENV LANGUAGE nl_NL:nl 
ENV LC_ALL nl_NL.UTF-8  
RUN update-locale LANG=nl_NL.UTF-8

WORKDIR /code
RUN mkdir -p /code/output/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app
COPY ./app/static /code/static/

CMD ["python", "app/main.py"]
