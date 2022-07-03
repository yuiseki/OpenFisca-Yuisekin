FROM python:3.8-bullseye
USER root

RUN apt update
RUN apt install -y \
    vim \
    htop \
    jq \
    curl

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir \
    autopep8 \
    flake8

WORKDIR /app
COPY . /app

RUN make install
RUN make build

RUN useradd -m user
USER user

EXPOSE 5000

CMD ["bash"]
