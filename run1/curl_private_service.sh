#!/bin/sh
#https://cloud.google.com/run/docs/triggering/https-request
privurl=$(gcloud run services describe private-service --format 'value(status.url)')
token=$(gcloud auth print-identity-token)
curl -H "Authorization: Bearer ${token}" $privurl
