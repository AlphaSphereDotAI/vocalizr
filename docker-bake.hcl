variable "IMAGE" {
  default = "ghcr.io/AlphaSphereDotAI/chatacter_backend_voice_generator"
}

target "default" {
  name = "chatacter_backend_voice_generator"
  context    = "."
  tags       = ["${IMAGE}:latest"] #,"${IMAGE}:dev"]
  dockerfile = "Dockerfile"
  platforms  = ["linux/amd64", "linux/arm64"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/AlphaSphereDotAI/chatacter_backend_voice_generator"
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
