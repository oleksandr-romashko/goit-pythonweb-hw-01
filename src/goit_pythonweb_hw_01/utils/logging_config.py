"""
Logging configuration module for the goit_pythonweb_hw_01 package.

This module provides a reusable function to set up basic logging
for any task or script in the project.
"""

import logging


def setup_logging():
    """Configure logging with console and file handlers."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
