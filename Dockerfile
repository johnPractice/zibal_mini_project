FROM ubuntu
RUN apt-get update
# RUN apt-get install -y build-essential  python3-pip python-dev   ffmpeg  ; 
RUN apt-get install -y python3-pip python-dev build-essential
WORKDIR /code/backend
COPY req.txt /code/backend/
EXPOSE 8000
RUN pip install --no-cache-dir -r req.txt
COPY . /code/backend/

# run cmd script
RUN chmod +x ./cmd.sh
CMD ["/bin/sh","./cmd.sh"]