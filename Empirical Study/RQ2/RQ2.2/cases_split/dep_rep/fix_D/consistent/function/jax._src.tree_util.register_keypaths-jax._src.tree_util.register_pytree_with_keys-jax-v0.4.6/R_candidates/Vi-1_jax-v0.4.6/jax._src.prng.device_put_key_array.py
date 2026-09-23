def device_put_key_array(x: PRNGKeyArray, device):
  return dispatch.device_put(x.unsafe_raw_array(), device)
