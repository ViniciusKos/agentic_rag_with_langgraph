from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

def create_workflow(agent_state, tools):
    """Create a workflow graph for the agent using the provided tools."""

    from .nodes import agent, analyze_documents, rewrite, generate


    workflow = StateGraph(agent_state)

    # Define nodes
    workflow.add_node("agent", lambda state: agent(state, tools))
    retrieve_node = ToolNode(tools)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("generate", generate)

    #Define the edges
    workflow.add_edge(START, "agent")

    workflow.add_conditional_edges("agent", 
                                  tools_condition,
                                  {"tools": "retrieve",
                                   END: END,
                                   },
                                   )

    # Edges after retrieval
    workflow.add_conditional_edges("retrieve", 
                                  analyze_documents,
                                    {"generate": "generate",
                                     "rewrite": "rewrite",
                                     },
                                     )

    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")

    return workflow.compile()