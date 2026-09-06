from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames

from config import WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL

# Credentials come from the environment -- see .env.example. Inside Skills
# Network's Cloud IDE the API key is injected for you, so WATSONX_API_KEY can
# stay unset there.
credentials = Credentials(url=WATSONX_URL, api_key=WATSONX_API_KEY)

# This script uses the text-generation API (model.generate), so these
# GenTextParamsMetaNames keys are the correct ones here -- unlike the Chat API
# used by model.py, which takes max_tokens/temperature instead.
params = {
    GenTextParamsMetaNames.DECODING_METHOD: "greedy",
    GenTextParamsMetaNames.MAX_NEW_TOKENS: 100,
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    params=params,
    credentials=credentials,
    project_id=WATSONX_PROJECT_ID,
)

text = """
Only reply with the answer. What is the capital of Canada?
"""

print(model.generate(text)["results"][0]["generated_text"])
