FROM python:3.8.1-alpine3.11
LABEL maintainer="code@tylerc.me"

RUN mkdir -p /usr/src/.local && mkdir -p /usr/src/app/files.d /usr/src/app/rules.d && chown -R guest:users /usr/src

USER guest
ENV PYTHONUSERBASE=/usr/src/.local PATH=$PATH:/usr/src/.local/bin
WORKDIR /usr/src/app

COPY MANIFEST.in ./
COPY setup.py ./

COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt
COPY nsa/ ./nsa
RUN pip install --user --no-cache-dir -e .

RUN nsa init --path /usr/src/app

ENTRYPOINT ["nsa"]
