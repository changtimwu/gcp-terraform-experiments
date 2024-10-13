#!/bin/sh
gcloud run services delete public-service
terraform plan
terraform apply
