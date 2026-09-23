def set_response_etag(response):
    if not response.streaming:
        response['ETag'] = quote_etag(hashlib.md5(response.content).hexdigest())
    return response
