def submit_build(pipeline_id, project_id, source_branch, source_version):
    print("Submitting build for branch: " + source_branch)
    print("Commit SHA1: ", source_version)

    run_build_raw = s.post(build_base_url, json={
        "definition": {"id": pipeline_id},
        "project": {"id": project_id},
        "sourceBranch": source_branch,
        "sourceVersion": source_version
    })

    try:
        run_build_json = run_build_raw.json()
    except json.decoder.JSONDecodeError as e:
        print(e)
        print("Failed to parse the response. Check if the Azure DevOps PAT is incorrect or expired.")
        sys.exit(-1)

    build_id = run_build_json['id']

    print("Submitted bulid: " + str(build_id))
    print("Bulid URL: " + run_build_json['url'])
    return build_id
