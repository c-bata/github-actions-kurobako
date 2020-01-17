# Container image that runs your code
FROM alpine:3.10

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

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
