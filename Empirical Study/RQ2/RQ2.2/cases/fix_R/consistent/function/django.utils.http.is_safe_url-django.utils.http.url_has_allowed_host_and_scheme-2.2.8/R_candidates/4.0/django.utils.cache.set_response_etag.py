def set_response_etag(response):
    if not response.streaming and response.content:
        response.headers['ETag'] = quote_etag(hashlib.md5(response.content).hexdigest())
    return response
