def add_tools_to_manager(toolmanager, tools=default_tools):
    """
    Add multiple tools to a `.ToolManager`.

    Parameters
    ----------
    toolmanager : `.backend_managers.ToolManager`
        Manager to which the tools are added.
    tools : {str: class_like}, optional
        The tools to add in a {name: tool} dict, see `add_tool` for more
        info.
    """

    for name, tool in tools.items():
        toolmanager.add_tool(name, tool)
