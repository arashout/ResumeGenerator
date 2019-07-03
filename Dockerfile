FROM python:3.6-alpine
COPY . /app
WORKDIR /app

RUN apk add --no-cache \
    xvfb \
    ttf-freefont \
    fontconfig \
    dbus \
    && \
    apk add qt5-qtbase-dev \
    wkhtmltopdf \
    --no-cache \
    --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
    --allow-untrusted \
    && \
    mv /usr/bin/wkhtmltopdf /usr/bin/wkhtmltopdf-origin && \
    echo $'#!/usr/bin/env sh\n\
    Xvfb :0 -screen 0 1024x768x24 -ac +extension GLX +render -noreset & \n\
    DISPLAY=:0.0 wkhtmltopdf-origin $@ \n\
    killall Xvfb\
    ' > /usr/bin/wkhtmltopdf && \
    chmod +x /usr/bin/wkhtmltopdf

RUN pip3 install -r requirements.txt
RUN ["python3", "main.py", "-o", "test.pdf", "resumes/resume.fs.yaml"]