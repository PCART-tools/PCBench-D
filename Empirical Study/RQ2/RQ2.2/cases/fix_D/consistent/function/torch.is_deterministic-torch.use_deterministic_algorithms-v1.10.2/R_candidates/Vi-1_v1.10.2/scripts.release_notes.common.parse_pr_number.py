def parse_pr_number(body, commit_hash, title):
    regex = r'Pull Request resolved: https://github.com/pytorch/pytorch/pull/([0-9]+)'
    matches = re.findall(regex, body)
    if len(matches) == 0:
        if 'revert' not in title.lower() and 'updating submodules' not in title.lower():
            print(f'[{commit_hash}: {title}] Could not parse PR number, ignoring PR')
        return None
    if len(matches) > 1:
        print(f'[{commit_hash}: {title}] Got two PR numbers, using the first one')
        return matches[0]
    return matches[0]
