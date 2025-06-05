import logging

from goit_pythonweb_hw_01.utils.logging_config import setup_logging

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("task 1")

    logger.info("Running task 1 example...")
    # task 1 code here
