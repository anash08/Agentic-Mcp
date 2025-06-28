import asyncio
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage, AIMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from graph import build_email_tool_graph, State
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "gmail": {
                "command": "python",
                "args": [
                    "./servers/gmail_server.py",
                    "--creds-file-path", "credentials.json",
                    "--token-path", "token.json"
                ],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    llm = ChatGroq(model="llama-3.1-8b-instant")
    graph = build_email_tool_graph(llm, tools)
    # Add a system prompt to control tool use
    system_message = SystemMessage(content=(
        "You are an assistant with access to email tools. "
        "Only call tools when the user requests an action. "
        "After a tool is called and the result is received, respond to the user in natural language and do not call more tools unless the user asks for another action."
        "For example, if the tool says 'Email sent successfully. Message ID: ...', tell the user 'Your email was sent successfully.' "

    ))
    user_message = "Send an email to kamalkaushik56@gmail.com with subject 'star trek31' and message 'Space the final frontier...'"
    state: State = {"messages": [system_message, user_message]}
    result = await graph.ainvoke(state)
    print("\n--- Final LLM Response ---")
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and msg.content:
            print(msg.content)

if __name__ == "__main__":
    asyncio.run(main()) 
    

