def get_ghstack_token():
    pattern = 'github_oauth = (.*)'
    with open(expanduser('~/.ghstackrc'), 'r+') as f:
        config = f.read()
    matches = re.findall(pattern, config)
    if len(matches) == 0:
        raise RuntimeError("Can't find a github oauth token")
    return matches[0]
