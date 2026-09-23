def urlsafe_base64_encode(s):
    """
    Encode a bytestring in base64 for use in URLs. Strip any trailing equal
    signs.
    """
    return base64.urlsafe_b64encode(s).rstrip(b'\n=')
