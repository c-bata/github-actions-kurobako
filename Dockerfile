FROM python:3.7.6-alpine3.11

RUN apk add --update gnuplot \
        fontconfig \
        ttf-ubuntu-font-family \
        msttcorefonts-installer \
        curl && \
    update-ms-fonts && \
    fc-cache -f && \
    rm -rf /var/cache/apk/*

RUN curl -L https://github.com/sile/kurobako/releases/download/0.1.4/kurobako-0.1.4.linux-amd64 -o kurobako && \
    chmod +x ./kurobako && \
    ./kurobako -h

RUN pip install PyGithub

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
