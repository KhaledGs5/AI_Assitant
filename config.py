import os
from pathlib import Path


def _load_dotenv(path=None):
    path = path or Path(__file__).with_name(".env")

    if not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, _, value = line.partition("=")

        key = key.strip()
        value = value.strip().strip("\"'")

        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


# Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# Generation parameters
PARAMETERS = {
    "temperature": 0,
    "max_tokens": 256,
}


# Models
LLAMA_MODEL_ID = os.environ.get(
    "LLAMA_MODEL_ID",
    "llama-3.1-8b-instant"
)

GRANITE_MODEL_ID = os.environ.get(
    "GRANITE_MODEL_ID",
    "openai/gpt-oss-20b"
)

MISTRAL_MODEL_ID = os.environ.get(
    "MISTRAL_MODEL_ID",
    "mistral-saba-24b"
)