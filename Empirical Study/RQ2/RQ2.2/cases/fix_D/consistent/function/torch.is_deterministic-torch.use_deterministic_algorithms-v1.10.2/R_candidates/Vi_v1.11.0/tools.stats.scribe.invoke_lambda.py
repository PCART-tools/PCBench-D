def invoke_lambda(name: str, payload: Any) -> Any:
    res = aws_lambda().invoke(FunctionName=name, Payload=json.dumps(payload).encode())
    payload = str(res["Payload"].read().decode())
    if res.get("FunctionError"):
        raise Exception(payload)
    return payload
