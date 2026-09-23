def device_put_transpose_rule(ct, _, device, src):
  return [device_put_p.bind(ct, device=src, src=device)]
