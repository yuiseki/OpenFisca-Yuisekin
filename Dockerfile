FROM python:3.8-bullseye
USER root

RUN apt update
RUN apt install -y \
    vim \
    htop \
    jq \
    curl

# Set locale
RUN apt-get install -y locales \
    && sed -i '/^#.* ja_JP.UTF-8 /s/^#//' /etc/locale.gen \
    && locale-gen \
    && ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime\
    && dpkg-reconfigure -f noninteractive tzdata
ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"

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
