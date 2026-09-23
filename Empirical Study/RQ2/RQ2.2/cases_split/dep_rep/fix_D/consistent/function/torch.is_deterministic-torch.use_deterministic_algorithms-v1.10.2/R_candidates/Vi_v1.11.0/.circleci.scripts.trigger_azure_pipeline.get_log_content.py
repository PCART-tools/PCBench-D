def get_log_content(url):
    resp = s.get(url)
    return resp.text
