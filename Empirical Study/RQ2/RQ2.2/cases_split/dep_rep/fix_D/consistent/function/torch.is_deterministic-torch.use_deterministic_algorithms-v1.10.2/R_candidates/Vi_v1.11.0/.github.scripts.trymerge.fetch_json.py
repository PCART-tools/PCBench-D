def fetch_json(url: str,
               params: Optional[Dict[str, Any]] = None,
               data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if params is not None and len(params) > 0:
        url += '?' + '&'.join(f"{name}={val}" for name, val in params.items())
    return cast(List[Dict[str, Any]], _fetch_url(url, headers=headers, data=data, reader=json.load))
