# wLw-Partner-Map

Automating updates to [wLw](https://wir-lernen-weiter.ch)'s [partner map](https://wir-lernen-weiter.ch/partnergemeinden/).

Contributed as part of [DINAcon HACKnights 2022](https://hacknight.dinacon.ch/event/8).

## Run locally

```sh
make setup
cd exporter
./run.sh
cd ../map
npm start
```

## Run on k8s

```sh
make images
# TODO
```
