output "private_url" {
  value = google_cloud_run_v2_service.private.uri
}
output "public_url" {
  value = google_cloud_run_v2_service.public.uri
}

