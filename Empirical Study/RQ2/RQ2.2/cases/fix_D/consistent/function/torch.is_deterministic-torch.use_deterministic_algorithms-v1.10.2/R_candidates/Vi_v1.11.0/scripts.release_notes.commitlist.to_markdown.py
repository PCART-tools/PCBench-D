def to_markdown(commit_list, category):
    def cleanup_title(commit):
        match = re.match(r'(.*) \(#\d+\)', commit.title)
        if match is None:
            return commit.title
        return match.group(1)

    cdc = CommitDataCache()
    lines = [f'\n## {category}\n']
    for topic in topics:
        lines.append(f'### {topic}\n')
        commits = commit_list.filter(category=category, topic=topic)
        for commit in commits:
            result = cleanup_title(commit)
            maybe_pr_number = cdc.get(commit.commit_hash).pr_number
            if maybe_pr_number is None:
                result = f'- {result} ({commit.commit_hash})\n'
            else:
                result = f'- {result} ([#{maybe_pr_number}](https://github.com/pytorch/pytorch/pull/{maybe_pr_number}))\n'
            lines.append(result)
    return lines
