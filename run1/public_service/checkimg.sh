#!/bin/sh
defprj=$(gcloud config get project)
defloc=$(gcloud config get artifacts/location)
reponam="samples"
imgnam="public-service-sample1"
gcloud artifacts docker images describe ${defloc}-docker.pkg.dev/${defprj}/${reponam}/${imgnam} --show-build-details --show-deployment
