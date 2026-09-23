def test_to_graphviz_attributes():
    assert to_graphviz(dsk).graph_attr['rankdir'] == 'BT'
    assert to_graphviz(dsk, rankdir='LR').graph_attr['rankdir'] == 'LR'
    assert to_graphviz(dsk, node_attr={'color': 'white'}).node_attr['color'] == 'white'
    assert to_graphviz(dsk, edge_attr={'color': 'white'}).edge_attr['color'] == 'white'
