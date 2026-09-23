def validate_flows(G, s, t, flowDict, solnValue, capacity, flow_func):
    errmsg = f"Assertion failed in function: {flow_func.__name__}"
    assert set(G) == set(flowDict), errmsg
    for u in G:
        assert set(G[u]) == set(flowDict[u]), errmsg
    excess = {u: 0 for u in flowDict}
    for u in flowDict:
        for v, flow in flowDict[u].items():
            if capacity in G[u][v]:
                assert flow <= G[u][v][capacity]
            assert flow >= 0, errmsg
            excess[u] -= flow
            excess[v] += flow
    for u, exc in excess.items():
        if u == s:
            assert exc == -solnValue, errmsg
        elif u == t:
            assert exc == solnValue, errmsg
        else:
            assert exc == 0, errmsg
