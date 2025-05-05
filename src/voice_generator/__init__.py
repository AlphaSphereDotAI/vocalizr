"""
Core constants and environment checks for the Voice Generator package.

Keeping this module tiny avoids pulling heavy dependencies into processes
that only need the shared constants (e.g. docs builders, CI linters).
"""

# `torch` is optional: gracefully fall back to CPU-only mode when it is absent.
try:
    import torch

    CUDA_AVAILABLE: bool = torch.cuda.is_available()
except ModuleNotFoundError:  # pragma: no cover – torch optional
    torch = None  # type: ignore
    CUDA_AVAILABLE = False

# Maximum allowed characters for TTS generation (`None` disables the cap).
CHAR_LIMIT: int | None = 5000

__all__ = ["CUDA_AVAILABLE", "CHAR_LIMIT"]
