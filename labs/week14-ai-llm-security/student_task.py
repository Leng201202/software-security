"""Output-sink control for the deterministic mock exercise.
Treat raw model output as untrusted text: redact the exact assigned secret,
then HTML-escape it for a text-node sink. This is not universal LLM safety.
"""
def render_model_output(raw, secret):
    raise NotImplementedError("implement redaction and HTML text escaping")
