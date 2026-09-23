def _filter_layers(layers, include_tags):
    if include_tags is None:
        return layers
    include_tags = set(include_tags)
    return [l for l in layers if not include_tags.isdisjoint(l.tags)]
