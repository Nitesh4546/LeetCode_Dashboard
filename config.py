"""
Centralized config. Reads from a .env file (or real env vars) so no
secrets/usernames are hardcoded in source.

Create a `.env` file next to this file:

    LEETCODE_API_URL=https://alfa-leetcode-api.onrender.com
    LEETCODE_USERNAME=your_leetcode_username
    CACHE_TTL_MINUTES=30
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # loads .env from the working directory if present

BASE_URL = os.getenv("LEETCODE_API_URL", "https://alfa-leetcode-api.onrender.com").rstrip("/")
USERNAME = os.getenv("LEETCODE_USERNAME", "").strip()
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "30"))

if not USERNAME:
    raise RuntimeError(
        "LEETCODE_USERNAME is not set. Create a .env file with "
        "LEETCODE_USERNAME=<your_username> (see config.py docstring)."
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)