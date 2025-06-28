from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.language_models import BaseChatModel

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def is_tool_call(state: State) -> str:
    """Route to 'tools' if the last message is an AIMessage with tool_calls, else to END."""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return END

def build_email_tool_graph(llm: BaseChatModel, tools: list):
    builder = StateGraph(State)
    # Node: LLM (bind tools!)
    def llm_node(state):
        # The system prompt should be included in the message history by the client
        print("\n--- DEBUG: Messages passed to LLM ---")
        for msg in state["messages"]:
            print(msg)
        return {
            "messages": [llm.bind_tools(tools).invoke(state["messages"])]
        }
    builder.add_node("llm", llm_node)
    # Node: Tools
    builder.add_node("tools", ToolNode(tools))
    # Edges
    builder.add_edge(START, "llm")
    builder.add_conditional_edges("llm", is_tool_call)
    builder.add_edge("tools", "llm")
    builder.set_finish_point("llm")
    return builder.compile()
