def get_flowcost_from_flowdict(G, flowDict):
    """Returns flow cost calculated from flow dictionary"""
    flowCost = 0
    for u in flowDict.keys():
        for v in flowDict[u].keys():
            flowCost += flowDict[u][v] * G[u][v]["weight"]
    return flowCost
