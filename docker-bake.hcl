variable "IMAGE" {
  default = "ghcr.io/alphaspheredotai/vocalizr"
}

target "build" {
  context    = "."
  tags       = ["${IMAGE}:latest"] #,"${IMAGE}:dev"]
  dockerfile = "Dockerfile"
#  platforms  = ["linux/amd64", "linux/arm64"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/AlphaSphereDotAI/vocalizr"
  }
  cache_from = [{ type = "gha" }]
  cache_to = [
    {
      type = "gha"
      mode = "max"
    }
  ]
  output = [{ type = "registry" }]
}

target "check" {
  inherits = ["build"]
  call = "check"
}