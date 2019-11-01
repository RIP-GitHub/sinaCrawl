FROM python:3.6

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /command

CMD [ "python", "user_run.py" ]