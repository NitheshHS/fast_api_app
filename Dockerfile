FROM python:3.10

WORKDIR /home/app

COPY requirements.txt /home/app

RUN python3 -m venv /home/app/venv

RUN /home/app/venv/bin/pip install --upgrade pip

RUN /home/app/venv/bin/pip install -r /home/app/requirements.txt

COPY . /home/app

EXPOSE 8000

CMD ["/home/app/venv/bin/uvicorn", "blogs.main:app", "--host", "0.0.0.0", "--port", "8000"]