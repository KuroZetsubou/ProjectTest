# syntax=docker/dockerfile:1
FROM node:12-alpine

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
RUN apk update

RUN apk add --no-cache python3 g++ make screen npm python3-dev mongodb curl yaml-cpp=0.6.2-r2

RUN npm install -g serve

WORKDIR /app
COPY . .

RUN python3 -m pip install wheel
RUN python3 -m pip install -r requirements.txt

CMD ["screen", "python3", "api/main.py"]
CMD ["screen", "serve", "web/public", "-p", "3000"]
# TODO SATELLITE

EXPOSE 3000 80 443 22