def get_disabled_issues() -> str:
    pr_body = os.getenv('PR_BODY', '')
    # The below regex is meant to match all *case-insensitive* keywords that
    # GitHub has delineated would link PRs to issues, more details here:
    # https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue.
    # E.g., "Close #62851", "fixES #62851" and "RESOLVED #62851" would all match, but not
    # "closes  #62851" --> extra space, "fixing #62851" --> not a keyword, nor "fix 62851" --> no #
    regex = '(?i)(Close(d|s)?|Resolve(d|s)?|Fix(ed|es)?) #([0-9]+)'
    issue_numbers = [x[4] for x in re.findall(regex, pr_body)]
    return ','.join(issue_numbers)
