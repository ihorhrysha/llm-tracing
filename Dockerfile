FROM python:3.12-slim-bookworm
WORKDIR /devops-hobbies
ENV FLASK_APP app.py
COPY src/requirements.txt . 
RUN pip3 install -r requirements.txt
COPY src/app.py .
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]