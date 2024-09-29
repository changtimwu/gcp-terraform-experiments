#!/bin/sh
#gcloud iam service-accounts list
#gcloud iam service-accounts keys list --iam-account=cloud-run-interservice-id@gen-lang-client-0633195184.iam.gserviceaccount.com
gcloud iam service-accounts keys create sakey.json --iam-account=cloud-run-interservice-id@gen-lang-client-0633195184.iam.gserviceaccount.com
