from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """Define o estado do agente usando TypedDict."""
    messages: Annotated[Sequence[BaseMessage], add_messages]