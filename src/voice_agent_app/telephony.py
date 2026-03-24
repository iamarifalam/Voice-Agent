from __future__ import annotations

from xml.sax.saxutils import escape


def gather_twiml(message: str, action_url: str) -> str:
    safe_message = escape(message)
    safe_action = escape(action_url)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f"<Gather input=\"speech\" action=\"{safe_action}\" method=\"POST\" speechTimeout=\"auto\">"
        f"<Say voice=\"Polly.Joanna\">{safe_message}</Say>"
        "</Gather>"
        "<Say voice=\"Polly.Joanna\">We did not receive speech input. Goodbye.</Say>"
        "</Response>"
    )


def say_twiml(message: str) -> str:
    safe_message = escape(message)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f"<Say voice=\"Polly.Joanna\">{safe_message}</Say>"
        "</Response>"
    )

