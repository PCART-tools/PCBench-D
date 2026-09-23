def parse_fuller_format(lines: Union[str, List[str]]) -> GitCommit:
    """
    Expect commit message generated using `--format=fuller --date=unix` format, i.e.:
        commit <sha1>
        Author:     <author>
        AuthorDate: <author date>
        Commit:     <committer>
        CommitDate: <committer date>

        <title line>

        <full commit message>

    """
    if isinstance(lines, str):
        lines = lines.split("\n")
    # TODO: Handle merge commits correctly
    if len(lines) > 1 and lines[1].startswith("Merge:"):
        del lines[1]
    assert len(lines) > 7
    assert lines[0].startswith("commit")
    assert lines[1].startswith("Author: ")
    assert lines[2].startswith("AuthorDate: ")
    assert lines[3].startswith("Commit: ")
    assert lines[4].startswith("CommitDate: ")
    assert len(lines[5]) == 0
    return GitCommit(commit_hash=lines[0].split()[1].strip(),
                     author=lines[1].split(":", 1)[1].strip(),
                     author_date=datetime.fromtimestamp(int(lines[2].split(":", 1)[1].strip())),
                     commit_date=datetime.fromtimestamp(int(lines[4].split(":", 1)[1].strip())),
                     title=lines[6].strip(),
                     body="\n".join(lines[7:]),
                     )
