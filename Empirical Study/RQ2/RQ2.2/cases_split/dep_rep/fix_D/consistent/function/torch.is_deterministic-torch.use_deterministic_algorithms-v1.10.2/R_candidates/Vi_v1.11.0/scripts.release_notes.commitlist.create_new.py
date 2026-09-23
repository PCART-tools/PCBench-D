def create_new(path, base_version, new_version):
    commits = CommitList.create_new(path, base_version, new_version)
    commits.write_to_disk()
