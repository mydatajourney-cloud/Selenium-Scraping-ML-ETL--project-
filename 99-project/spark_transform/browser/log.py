# log.py
import logging
import os

def log_bad_referer(domain, url):
    logger.info(f"Unknown referer: domain={domain}, url={url}")

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logger = logging.getLogger("referer_logger")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler("logs/bad_referers.log")
file_handler.setLevel(logging.INFO)

# Format
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger (avoid adding multiple times)
if not logger.hasHandlers():
    logger.addHandler(file_handler)

