FROM ubuntu:16.04

ARG ssh_prv_key

ENV DEBIAN_FRONTEND noninteractive
ENV APT_QUIET "apt-get -yqq -o=Dpkg::Use-Pty=0"
ENV FILE_SOURCE .

RUN $APT_QUIET update && \
    $APT_QUIET install --no-install-recommends apt-utils && \
    $APT_QUIET upgrade && \
    $APT_QUIET install build-essential vim tmux htop python3 python3-pip git

RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install django==2.0.4 django-import-export==1.0.1 \
    geojson==2.4.0 shapely==1.6.4.post2

RUN git clone https://github.com/PederBG/PolyMap.git

ENTRYPOINT  /bin/bash -c 'tmux new-session -d -s "django" "cd /root/polymap && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver && tmux detach" && cd /root/polymap && /bin/bash'
