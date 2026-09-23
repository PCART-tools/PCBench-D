    def update(self, params: QueryParamTypes = None) -> None:
        if not params:
            return

        params = QueryParams(params)
        for param in params:
            item, *extras = params.get_list(param)
            self[param] = item
            if extras:
                self._list.extend((param, e) for e in extras)
                # ensure getter matches merged QueryParams getter
                self._dict[param] = params[param]
