terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_container" "health_monitor" {
  name  = "health-monitor-terraform"
  image = "health-monitor:1.0"

  ports {
    internal = 8000
    external = 8002
    ip       = "127.0.0.1"
  }
}
