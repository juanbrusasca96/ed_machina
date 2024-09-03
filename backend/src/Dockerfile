FROM python:3.11

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt

EXPOSE 8002

# copy project
COPY . /usr/src/
CMD ["uvicorn", "main:app", "--proxy-headers","--reload","--workers","1", "--host", "0.0.0.0", "--port", "8002"]