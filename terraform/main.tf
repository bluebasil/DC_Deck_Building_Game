terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── Artifact Registry repository ─────────────────────────────────────────────
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.service_name
  description   = "DC Deck Builder container images"
  format        = "DOCKER"
}

# ── Cloud Run service ─────────────────────────────────────────────────────────
resource "google_cloud_run_v2_service" "game" {
  name     = var.service_name
  location = var.region

  template {
    scaling {
      min_instance_count = 0   # Scale to zero when idle — free tier
      max_instance_count = 1   # Single instance per concurrent game
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.service_name}/${var.service_name}:${var.image_tag}"

      ports {
        container_port = 8080
      }

      #env {
      #  name  = "PORT"
      #  value = "8080"
      #}
      env {
        name  = "USE_GEVENT"
        value = "1"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        # Only charge when actively handling requests
        cpu_idle = false
      }
    }

    # Allow long-lived WebSocket connections (60 min timeout)
    timeout = "3600s"
  }

  # Required for WebSockets on Cloud Run
  client = "terraform"
}

# ── Allow unauthenticated public access ──────────────────────────────────────
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.game.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
