import re

USER_AGENT_RE = re.compile(r"^User-agent: .+", re.IGNORECASE)
ALLOW_RE = re.compile(r"^(Allow|Disallow): .+", re.IGNORECASE)


def validate_llms(content: str) -> bool:
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    if not lines:
        return False
    for line in lines:
        if USER_AGENT_RE.match(line):
            continue
        if ALLOW_RE.match(line):
            continue
        # allow comments
        if line.startswith('#'):
            continue
        return False
    return True