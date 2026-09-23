def build_node(layer):
    layer_name = layer.layer_name.replace("|", "\\|")
    label = f"{{{layer_name}|kernel: {layer.kernel_name}\\l|tactic: {layer.tactic}\\l|time: {layer.time}\\l}}"
    label = label.replace(">", "\\>")
    return pydot.Node(layer.layer_name, label=label, **style)
