
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

MARKLOGIC_BASE_URL = os.getenv("MARKLOGIC_BASE_URL")
MARKLOGIC_USERNAME = os.getenv("MARKLOGIC_USERNAME")
MARKLOGIC_PASSWORD = os.getenv("MARKLOGIC_PASSWORD")


def get_marklogic_client():
    if not all([
        MARKLOGIC_BASE_URL,
        MARKLOGIC_USERNAME,
        MARKLOGIC_PASSWORD
    ]):
        raise RuntimeError("MarkLogic configuration is missing")

    with httpx.Client(
        base_url=MARKLOGIC_BASE_URL,
        auth=httpx.DigestAuth(
            MARKLOGIC_USERNAME,
            MARKLOGIC_PASSWORD
        ),
        timeout=10.0
    ) as client:
        yield client
