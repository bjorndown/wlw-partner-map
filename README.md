# wLw-Partner-Map

Automating updates to [wLw](https://wir-lernen-weiter.ch)'s [partner map](https://wir-lernen-weiter.ch/partnergemeinden/).

Contributed as part of [DINAcon HACKnights 2022](https://hacknight.dinacon.ch/event/8).

## Requirements

Install Python 3.9+, SQLite3 and Node.js/NPM 14+ before starting.

## Run locally

```sh
make setup
make run-exporter
make run-map
```

## Run with docker/podman

```sh
make setup
make images
make run-exporter-container
make run-map-container
# open http://localhost:8080
```
