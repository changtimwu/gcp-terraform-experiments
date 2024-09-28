#!/bin/sh
#gcloud artifacts repositories create samples --repository-format docker
gcloud builds submit --config cloudbuild.yaml .
defprj=$(gcloud config get project)
defloc=$(gcloud config get artifacts/location)
reponam="samples"
#gcloud artifacts docker images describe ${defloc}-docker.pkg.dev/${defprj}/${reponam}/public-service-sample1

