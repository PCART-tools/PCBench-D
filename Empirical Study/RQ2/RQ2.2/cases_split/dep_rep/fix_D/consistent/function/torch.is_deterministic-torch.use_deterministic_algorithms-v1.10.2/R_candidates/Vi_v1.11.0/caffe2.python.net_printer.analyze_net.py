@Analyzer.register(Net)
def analyze_net(analyzer, net):
    for x in net.Proto().op:
        analyzer(x)
