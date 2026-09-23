def _format_msg(msg, payloads):
  payload_mapping = {}
  for i, pl in enumerate(payloads):
    payload_mapping[f'payload{i}'] = pl
  return msg.format(**payload_mapping)
