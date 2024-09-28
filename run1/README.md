## Purpose
We create a public and private cloud run service to check if the so-called `cloud run to cloud run` communication really works.

## Prepare the images 
* build the public service image with cloud build
```
cd public_service
./cbuild.sh
```
* check the built image and write down the image link
```
./checkimg.sh
```

* fill in `terraform.tfvars`
```tf
region = "<your region>"
project = "<your project>"
public_service_image = "<image link>"
```

## Deployment 
```
terraform init
terraform plan
terraform deploy
```

## Check result
```
% gcloud run services describe public-service
✔ Service public-service in region asia-east1
goog-terraform-provisioned:true

URL:     https://public-service-xxxxx.asia-east1.run.app
Ingress: all
Traffic:
  100% LATEST (currently public-service-00001-7hw)

Last updated on 2024-09-28T21:02:45.224633Z by xx:
  Revision public-service-00001-7hw
  Container None
    Image:           <image link>
    Port:            8080
    Memory:          512Mi
    CPU:             1000m
    Env vars:
      targetURL      https://private-service-xxxxx-de.a.run.app
    Startup Probe:
      TCP every 240s
      Port:          8080
      Initial delay: 0s
      Timeout:       240s
      Failure threshold: 1
      Type:          Default
  Service account:   cloud-run-interservice-id@<ypur project>.iam.gserviceaccount.com
  Concurrency:       80
  Min Instances:     0
  Max Instances:     100
  Timeout:           300s
  Session Affinity:  false


% gcloud run services get-iam-policy private-service
bindings:
- members:
  - serviceAccount:cloud-run-interservice-id@<your project>.iam.gserviceaccount.com
  role: roles/run.invoker
etag: BwYjKZFxvpU=
version: 1
```
