FROM alpine:3.11

ARG KUROBAKO_VERSION=0.2.0

RUN apk add --update gnuplot \
        fontconfig \
        ttf-ubuntu-font-family \
        msttcorefonts-installer \
        curl && \
    update-ms-fonts && \
    fc-cache -f && \
    rm -rf /var/cache/apk/*

RUN curl -L https://github.com/sile/kurobako/releases/download/${KUROBAKO_VERSION}/kurobako-${KUROBAKO_VERSION}.linux-amd64 -o kurobako && \
    chmod +x ./kurobako && \
    ./kurobako -h

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
