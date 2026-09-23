def send_message(messages: List[Dict[str, Any]]) -> None:
    logs = json.dumps(
        [
            {
                "category": "perfpipe_pytorch_binary_size",
                "message": json.dumps(message),
                "line_escape": False,
            }
            for message in messages
        ]
    )
    res = send_to_scribe(logs)
    print(res)
