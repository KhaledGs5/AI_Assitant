"""Smoke test: call all three models and print their parsed JSON replies."""

import json

from model import llama_response, granite_response, mistral_response


def call_all_models(system_prompt, user_prompt):
    # Each *_response returns the parsed JSON dict (summary / sentiment /
    # response), not a message object -- so print the dict, not `.content`.
    for name, fn in (
        ("Llama", llama_response),
        ("Granite", granite_response),
        ("Mistral", mistral_response),
    ):
        print(f"\n{name} Response:")
        try:
            print(json.dumps(fn(system_prompt, user_prompt), indent=2))
        except Exception as exc:
            print(f"  failed: {exc}")


if __name__ == "__main__":
    call_all_models(
        "You are a helpful assistant who provides concise and accurate answers",
        "What is the capital of Canada? Tell me a cool fact about it as well",
    )
