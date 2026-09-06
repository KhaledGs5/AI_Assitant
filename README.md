# GenAI Flask App

A small Flask UI that sends one customer message to three watsonx.ai models
(Llama, Granite, Mistral) and shows each model's summary, sentiment score, and
suggested reply side by side.

## Run it

The repo already contains a `venv` (Python 3.10.11) with every dependency
installed. From the project root in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

Or without activating the virtualenv:

```powershell
.\venv\Scripts\python.exe app.py
```

Then open <http://127.0.0.1:5000>. `debug=True` is set in `app.py`, so edits
reload automatically. Press Ctrl+C to stop.

If PowerShell blocks `Activate.ps1`, either use the direct
`venv\Scripts\python.exe` form above or run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

## Credentials

Inside Skills Network's Cloud IDE the watsonx API key is injected for you and
the shared `skills-network` project is used, so no setup is needed.

To run anywhere else, copy the template and fill in your own values:

```powershell
Copy-Item .env.example .env
```

Then set at minimum `WATSONX_API_KEY` (create one at
<https://cloud.ibm.com/iam/apikeys>) and `WATSONX_PROJECT_ID` (in watsonx.ai:
**Manage → General → Project ID**). Real environment variables override `.env`,
so `$env:WATSONX_API_KEY = "..."` also works for a one-off run.

`config.py` reads `.env` itself, so no extra dependency is required. `.env` is
gitignored — never commit a real key.

Without credentials the app still starts and serves the page; the failure shows
up as an error message in the chat when you send a request, naming what to set.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Flask routes: `/` renders the UI, `POST /generate` calls a model |
| `model.py` | watsonx clients, per-model prompt templates, JSON output parsing |
| `config.py` | Credentials from the environment, generation params, model ids |
| `llm_test.py` | Command-line smoke test that calls all three models |
| `capital.py` | Standalone text-generation example (not used by the app) |
| `templates/`, `static/` | UI markup, stylesheet, and browser JavaScript |

## Notes

- The three model ids in `config.py` must be available in your watsonx region,
  or `/generate` returns a 500 for that model. Override them with
  `LLAMA_MODEL_ID`, `GRANITE_MODEL_ID`, or `MISTRAL_MODEL_ID`.
- `model.py` talks to the **Chat** API, so `config.PARAMETERS` uses
  `temperature`/`max_tokens`. `capital.py` uses the **text-generation** API,
  where `decoding_method`/`max_new_tokens` are the correct keys instead.
- Responses are parsed into `{summary, sentiment, response}`. A model that
  replies with malformed JSON raises a parse error, surfaced in the UI.
