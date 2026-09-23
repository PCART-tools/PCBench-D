def update_existing(path, new_version):
    commits = CommitList.from_existing(path)
    commits.update_to(new_version)
    commits.write_to_disk()
