def _to_graphviz(
    tree_info: Dict[str, Any],
    show_info: List[str],
    feature_names: Union[List[str], None],
    precision: Optional[int] = 3,
    orientation: str = 'horizontal',
    constraints: Optional[List[int]] = None,
    **kwargs: Any
) -> Any:
    """Convert specified tree to graphviz instance.

    See:
      - https://graphviz.readthedocs.io/en/stable/api.html#digraph
    """
    if GRAPHVIZ_INSTALLED:
        from graphviz import Digraph
    else:
        raise ImportError('You must install graphviz and restart your session to plot tree.')

    def add(root, total_count, parent=None, decision=None):
        """Recursively add node or edge."""
        if 'split_index' in root:  # non-leaf
            l_dec = 'yes'
            r_dec = 'no'
            if root['decision_type'] == '<=':
                lte_symbol = "&#8804;"
                operator = lte_symbol
            elif root['decision_type'] == '==':
                operator = "="
            else:
                raise ValueError('Invalid decision type in tree model.')
            name = f"split{root['split_index']}"
            if feature_names is not None:
                label = f"<B>{feature_names[root['split_feature']]}</B> {operator}"
            else:
                label = f"feature <B>{root['split_feature']}</B> {operator} "
            label += f"<B>{_float2str(root['threshold'], precision)}</B>"
            for info in ['split_gain', 'internal_value', 'internal_weight', "internal_count", "data_percentage"]:
                if info in show_info:
                    output = info.split('_')[-1]
                    if info in {'split_gain', 'internal_value', 'internal_weight'}:
                        label += f"<br/>{_float2str(root[info], precision)} {output}"
                    elif info == 'internal_count':
                        label += f"<br/>{output}: {root[info]}"
                    elif info == "data_percentage":
                        label += f"<br/>{_float2str(root['internal_count'] / total_count * 100, 2)}% of data"

            fillcolor = "white"
            style = ""
            if constraints:
                if constraints[root['split_feature']] == 1:
                    fillcolor = "#ddffdd"  # light green
                if constraints[root['split_feature']] == -1:
                    fillcolor = "#ffdddd"  # light red
                style = "filled"
            label = f"<{label}>"
            graph.node(name, label=label, shape="rectangle", style=style, fillcolor=fillcolor)
            add(root['left_child'], total_count, name, l_dec)
            add(root['right_child'], total_count, name, r_dec)
        else:  # leaf
            name = f"leaf{root['leaf_index']}"
            label = f"leaf {root['leaf_index']}: "
            label += f"<B>{_float2str(root['leaf_value'], precision)}</B>"
            if 'leaf_weight' in show_info:
                label += f"<br/>{_float2str(root['leaf_weight'], precision)} weight"
            if 'leaf_count' in show_info:
                label += f"<br/>count: {root['leaf_count']}"
            if "data_percentage" in show_info:
                label += f"<br/>{_float2str(root['leaf_count'] / total_count * 100, 2)}% of data"
            label = f"<{label}>"
            graph.node(name, label=label)
        if parent is not None:
            graph.edge(parent, name, decision)

    graph = Digraph(**kwargs)
    rankdir = "LR" if orientation == "horizontal" else "TB"
    graph.attr("graph", nodesep="0.05", ranksep="0.3", rankdir=rankdir)
    if "internal_count" in tree_info['tree_structure']:
        add(tree_info['tree_structure'], tree_info['tree_structure']["internal_count"])
    else:
        raise Exception("Cannot plot trees with no split")

    if constraints:
        # "#ddffdd" is light green, "#ffdddd" is light red
        legend = """<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
             <TR>
              <TD COLSPAN="2"><B>Monotone constraints</B></TD>
             </TR>
             <TR>
              <TD>Increasing</TD>
              <TD BGCOLOR="#ddffdd"></TD>
             </TR>
             <TR>
              <TD>Decreasing</TD>
              <TD BGCOLOR="#ffdddd"></TD>
             </TR>
            </TABLE>
           >"""
        graph.node("legend", label=legend, shape="rectangle", color="white")
    return graph
