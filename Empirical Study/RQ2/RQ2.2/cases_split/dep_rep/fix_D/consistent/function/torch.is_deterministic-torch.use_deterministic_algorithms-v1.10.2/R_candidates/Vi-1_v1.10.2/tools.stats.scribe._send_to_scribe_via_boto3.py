def _send_to_scribe_via_boto3(logs: str) -> str:
    sprint("Scribe access token not provided, sending report via boto3...")
    event = {"base64_bz2_logs": base64.b64encode(bz2.compress(logs.encode())).decode()}
    return str(invoke_lambda("gh-ci-scribe-proxy", event))
