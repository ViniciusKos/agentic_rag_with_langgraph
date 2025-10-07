from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

def create_workflow(agent_state, tools):
    """Create a workflow graph for the agent using the provided tools."""
    graph = StateGraph()

    # Define the start and end nodes
    graph.add_node(START)
    graph.add_node(END)

    # Add a tool node to the graph
    tool_node = ToolNode("tool_node", tools=tools, state=agent_state)
    graph.add_node(tool_node)

    # Define the transitions between nodes
    graph.add_edge(START, tool_node)
    graph.add_edge(tool_node, END, condition=tools_condition(tool_node))

    return graph