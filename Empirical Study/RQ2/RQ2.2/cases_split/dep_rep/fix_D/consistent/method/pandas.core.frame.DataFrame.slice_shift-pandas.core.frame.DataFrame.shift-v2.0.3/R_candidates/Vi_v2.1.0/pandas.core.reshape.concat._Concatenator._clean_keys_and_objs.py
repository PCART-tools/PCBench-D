    def _clean_keys_and_objs(
        self,
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        keys,
    ) -> tuple[list[Series | DataFrame], Index | None]:
        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = list(objs.keys())
            objs_list = [objs[k] for k in keys]
        else:
            objs_list = list(objs)

        if len(objs_list) == 0:
            raise ValueError("No objects to concatenate")

        if keys is None:
            objs_list = list(com.not_none(*objs_list))
        else:
            # GH#1649
            clean_keys = []
            clean_objs = []
            if is_iterator(keys):
                keys = list(keys)
            if len(keys) != len(objs_list):
                # GH#43485
                warnings.warn(
                    "The behavior of pd.concat with len(keys) != len(objs) is "
                    "deprecated. In a future version this will raise instead of "
                    "truncating to the smaller of the two sequences",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            for k, v in zip(keys, objs_list):
                if v is None:
                    continue
                clean_keys.append(k)
                clean_objs.append(v)
            objs_list = clean_objs

            if isinstance(keys, MultiIndex):
                # TODO: retain levels?
                keys = type(keys).from_tuples(clean_keys, names=keys.names)
            else:
                name = getattr(keys, "name", None)
                keys = Index(clean_keys, name=name, dtype=getattr(keys, "dtype", None))

        if len(objs_list) == 0:
            raise ValueError("All objects passed were None")

        return objs_list, keys
