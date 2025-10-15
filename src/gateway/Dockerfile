FROM traefik:3.3.6

COPY ./src/gateway/acme.json /letsencrypt/acme.json

COPY ./src/gateway/traefik.yml /etc/traefik/traefik.yml

RUN chmod 600 /letsencrypt/acme.json
