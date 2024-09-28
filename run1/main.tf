terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "6.4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "6.4.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.region
}

resource "google_cloud_run_v2_service" "public" {
  name     = "public-service"
  location = var.region
  deletion_protection = false # set to "true" in production

  template {
    containers {
      # TODO<developer>: replace this with a public service container
      # (This service can be invoked by anyone on the internet)
      image = "asia-east1-docker.pkg.dev/gen-lang-client-0633195184/cloud-run-source-deploy/call-private"

      # Include a reference to the private Cloud Run
      # service's URL as an environment variable.
      env {
        name  = "targetURL"
        value = google_cloud_run_v2_service.private.uri
      }
    }
    # Give the "public" Cloud Run service
    # a service account's identity
    service_account = google_service_account.default.email
  }
}


# [END cloudrun_service_interservice_public_service]

resource "google_cloud_run_service_iam_policy" "public" {
  location = google_cloud_run_v2_service.public.location
  project  = google_cloud_run_v2_service.public.project
  service  = google_cloud_run_v2_service.public.name

  policy_data = data.google_iam_policy.public.policy_data
}
# [END cloudrun_service_interservice_public_policy]

# [START cloudrun_service_interservice_sa]
resource "google_service_account" "default" {
  account_id   = "cloud-run-interservice-id"
  description  = "Identity used by a public Cloud Run service to call private Cloud Run services."
  display_name = "cloud-run-interservice-id"
}

resource "google_cloud_run_v2_service" "private" {
  name     = "private-service"
  location = var.region

  deletion_protection = false # set to "true" in production

  template {
    containers {
      // TODO<developer>: replace this with a private service container
      // (This service should only be invocable by the public service)
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }
}

resource "google_cloud_run_service_iam_policy" "private" {
  location = google_cloud_run_v2_service.private.location
  project  = google_cloud_run_v2_service.private.project
  service  = google_cloud_run_v2_service.private.name
  policy_data = data.google_iam_policy.private.policy_data
}
