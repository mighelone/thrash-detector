FROM python:3.8.2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend frontend
COPY backend backend
COPY recycleye recycleye

CMD [ "gunicorn", "--workers=2", "frontend.app:app", "-b", ":8000" ]