def _create_arg_dict(self, a):
    r = {}
    for k, v in a.items():
        if not isinstance(k, str):
            # Check for invalid dict keys. We do not want a Proxy to appear
            # anywhere within the key. Since keys can be collection types,
            # we iterate through the key with map_arg
            k = self.create_arg(k)
            map_arg(k, _no_nodes_error)
        r[k] = self.create_arg(v)
    return r
