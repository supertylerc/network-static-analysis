# stdlib
from urllib.parse import urlparse

# third-party packages
from schema import And, Optional, Or, Schema, Use


VIOLATION_SCHEMA = Schema(
    [
        {
            "title": And(str, len),
            "device": And(str, len),
            "platforms": And(
                list, len, lambda l: all(isinstance(i, str) for i in l)
            ),
            "link": And(str, Use(str.lower), lambda u: urlparse(u)),
            "ticket": str,
            "reason": str,
            "previous_lines": And(
                list, lambda l: all(isinstance(i, str) for i in l)
            ),
            "match": And(str, len),
            "next_lines": And(
                list, lambda l: all(isinstance(i, str) for i in l)
            ),
            "wiki": str,
            Optional("cve"): And(str, Use(str.upper)),
            Optional("score"): And(Or(int, float), lambda n: n > 0),
        }
    ]
)

INPUT_SCHEMA = Schema(
    {
        "device": And(str, len),
        "platform": And(str, len),
        "contents": And(list, len),
    }
)
