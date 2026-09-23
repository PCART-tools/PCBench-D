def test_to_graphviz_attributes():
    assert to_graphviz(dsk).graph_attr['rankdir'] == 'BT'
    assert to_graphviz(dsk, rankdir='LR').graph_attr['rankdir'] == 'LR'
