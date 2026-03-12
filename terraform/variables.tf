variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "website-489802"
}

variable "region" {
  description = "GCP region for Cloud Run"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "dc-deck-builder"
}

variable "image_tag" {
  description = "Docker image tag (set by deploy script)"
  type        = string
  default     = "latest"
}
