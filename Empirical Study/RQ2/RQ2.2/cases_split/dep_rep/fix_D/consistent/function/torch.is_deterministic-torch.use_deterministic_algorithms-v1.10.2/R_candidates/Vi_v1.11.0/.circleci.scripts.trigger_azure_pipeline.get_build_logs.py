def get_build_logs(_id):
    get_build_logs_url = AZURE_PIPELINE_BASE_URL + f"/_apis/build/builds/{_id}/logs?api-version=6.0"
    get_build_logs_raw = s.get(get_build_logs_url)
    return get_build_logs_raw.json()
