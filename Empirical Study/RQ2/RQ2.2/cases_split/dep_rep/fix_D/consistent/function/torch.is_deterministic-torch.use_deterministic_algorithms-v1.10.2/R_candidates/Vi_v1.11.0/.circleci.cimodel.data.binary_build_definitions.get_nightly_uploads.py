def get_nightly_uploads():
    configs = gen_build_env_list(False)
    mylist = []
    for conf in configs:
        phase_dependency = "test" if predicate_exclude_macos(conf) else "build"
        mylist.append(conf.gen_upload_job("upload", phase_dependency))

    return mylist
