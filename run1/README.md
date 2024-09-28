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
```
