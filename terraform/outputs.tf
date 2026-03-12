output "service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.game.uri
}

output "image_repo" {
  description = "Artifact Registry image path prefix"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.service_name}/${var.service_name}"
}
