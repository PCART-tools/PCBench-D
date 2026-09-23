def _bidirectional_pred_succ(G, source, target, exclude):
    # does BFS from both source and target and meets in the middle
    # excludes nodes in the container "exclude" from the search
    if source is None or target is None:
        raise nx.NetworkXException(
            "Bidirectional shortest path called without source or target"
        )
    if target == source:
        return ({target: None}, {source: None}, source)

    # handle either directed or undirected
    if G.is_directed():
        Gpred = G.predecessors
        Gsucc = G.successors
    else:
        Gpred = G.neighbors
        Gsucc = G.neighbors

    # predecesssor and successors in search
    pred = {source: None}
    succ = {target: None}

    # initialize fringes, start with forward
    forward_fringe = [source]
    reverse_fringe = [target]

    level = 0

    while forward_fringe and reverse_fringe:
        # Make sure that we iterate one step forward and one step backwards
        # thus source and target will only trigger "found path" when they are
        # adjacent and then they can be safely included in the container 'exclude'
        level += 1
        if not level % 2 == 0:
            this_level = forward_fringe
            forward_fringe = []
            for v in this_level:
                for w in Gsucc(v):
                    if w in exclude:
                        continue
                    if w not in pred:
                        forward_fringe.append(w)
                        pred[w] = v
                    if w in succ:
                        return pred, succ, w  # found path
        else:
            this_level = reverse_fringe
            reverse_fringe = []
            for v in this_level:
                for w in Gpred(v):
                    if w in exclude:
                        continue
                    if w not in succ:
                        succ[w] = v
                        reverse_fringe.append(w)
                    if w in pred:
                        return pred, succ, w  # found path

    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")
