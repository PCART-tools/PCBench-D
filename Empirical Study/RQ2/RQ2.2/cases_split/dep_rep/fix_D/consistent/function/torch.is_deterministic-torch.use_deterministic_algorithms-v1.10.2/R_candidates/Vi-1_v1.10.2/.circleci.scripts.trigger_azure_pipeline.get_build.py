def get_build(_id):
    get_build_url = AZURE_PIPELINE_BASE_URL + f"/_apis/build/builds/{_id}?api-version=6.0"
    get_build_raw = s.get(get_build_url)
    return get_build_raw.json()
