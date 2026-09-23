def _not_modified(request, response=None):
    new_response = HttpResponseNotModified()
    if response:
        # Preserve the headers required by Section 4.1 of RFC 7232, as well as
        # Last-Modified.
        for header in ('Cache-Control', 'Content-Location', 'Date', 'ETag', 'Expires', 'Last-Modified', 'Vary'):
            if header in response:
                new_response[header] = response[header]

        # Preserve cookies as per the cookie specification: "If a proxy server
        # receives a response which contains a Set-cookie header, it should
        # propagate the Set-cookie header to the client, regardless of whether
        # the response was 304 (Not Modified) or 200 (OK).
        # https://curl.haxx.se/rfc/cookie_spec.html
        new_response.cookies = response.cookies
    return new_response
