def check_multihost_collective_allowlist(jaxpr):
  used_collectives = set(xla.jaxpr_collectives(jaxpr))
  if not used_collectives.issubset(multi_host_supported_collectives):
    bad_collectives = used_collectives - multi_host_supported_collectives
    msg = "using collectives that aren't supported for multi-host: {}"
    raise TypeError(msg.format(", ".join(map(str, bad_collectives))))
