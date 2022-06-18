FROM python:3.7

WORKDIR /app
COPY . /app

RUN make install
RUN make build

EXPOSE 5000

CMD ["make", "serve-local"]
