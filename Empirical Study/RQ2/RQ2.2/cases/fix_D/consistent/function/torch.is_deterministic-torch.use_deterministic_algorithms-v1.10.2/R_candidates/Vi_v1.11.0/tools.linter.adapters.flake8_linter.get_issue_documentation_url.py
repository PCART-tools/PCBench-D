def get_issue_documentation_url(code: str) -> str:
    if code in DOCUMENTED_IN_FLAKE8RULES:
        return f"https://www.flake8rules.com/rules/{code}.html"

    if code in DOCUMENTED_IN_FLAKE8COMPREHENSIONS:
        return "https://pypi.org/project/flake8-comprehensions/#rules"

    if code in DOCUMENTED_IN_BUGBEAR:
        return "https://github.com/PyCQA/flake8-bugbear#list-of-warnings"

    return ""
