    def _get_proxy_map(
        self, proxies: typing.Optional[ProxiesTypes], allow_env_proxies: bool
    ) -> typing.Dict[str, typing.Optional[Proxy]]:
        if proxies is None:
            if allow_env_proxies:
                return {
                    key: None if url is None else Proxy(url=url)
                    for key, url in get_environment_proxies().items()
                }
            return {}
        if isinstance(proxies, dict):
            new_proxies = {}
            for key, value in proxies.items():
                proxy = Proxy(url=value) if isinstance(value, (str, URL)) else value
                new_proxies[str(key)] = proxy
            return new_proxies
        else:
            proxy = Proxy(url=proxies) if isinstance(proxies, (str, URL)) else proxies
            return {"all://": proxy}
