#!/usr/bin/env python3
"""Development server script."""

import sys
import os
import uvicorn

# Add the parent directory to the path so we can import main
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.common.config import get_settings
from src.common.logging import setup_logging

# Setup logging
setup_logging()

# Get settings
settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
        access_log=True
    )