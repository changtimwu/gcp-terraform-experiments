#!/bin/sh
#gcloud artifacts repositories create samples --repository-format docker
gcloud builds submit --config cloudbuild.yaml .

