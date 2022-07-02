FROM python:3.7

RUN apt install vim

WORKDIR /app
COPY . /app

RUN make install
RUN make build

RUN useradd -m user
USER user

EXPOSE 5000

CMD ["bash"]
