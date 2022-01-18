FROM python:3.10.1-bullseye
LABEL maintainer="melanie.sigl@fau.de"

RUN python -m pip install --upgrade pip
COPY src/requirements.txt /tmp/.
RUN pip3 install -r /tmp/requirements.txt

ENTRYPOINT ["/bin/bash"]
