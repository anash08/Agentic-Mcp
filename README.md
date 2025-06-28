# MCP (Model Context Protocol) Project

This project demonstrates the integration of MCP (Model Context Protocol) servers and clients using LangChain, LangGraph, and the `langchain-mcp-adapters` library. It includes a math server for basic calculations and a Gmail server for email management operations.

## Features

- **Multi-Server MCP Setup**: Connect to multiple MCP servers simultaneously
- **Math Server**: Basic mathematical operations and calculations
- **Gmail Server**: Full email management including send, read, trash, and mark as read
- **LangGraph Integration**: StateGraph-based tool calling loop with proper message state management
- **Groq LLM Integration**: Uses ChatGroq as the LLM model instead of OpenAI

## Project Structure

```
mcp/
├── client.py              # Main MCP client with LangGraph integration
├── graph.py               # LangGraph StateGraph implementation
├── requirements.txt       # Python dependencies
├── servers/
│   ├── gmail_server.py    # Gmail MCP server
│   └── math_server.py     # Math MCP server
└── mcpEnv/               # Virtual environment
```

## Prerequisites

1. **Python 3.8+**
2. **Google Cloud Console Setup** (for Gmail server):
   - Create a project in Google Cloud Console
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download `credentials.json`

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/mcp
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv mcpEnv
   # On Windows:
   mcpEnv\Scripts\activate
   # On macOS/Linux:
   source mcpEnv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Gmail Server Setup

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Choose "Desktop application"
6. Download the credentials file and rename it to `credentials.json`
7. Place `credentials.json` in your project root

### 2. Generate Access Token

Run the Gmail server to generate your access token:

```bash
python servers/gmail_server.py --creds-file-path credentials.json --token-path token.json
```

This will:
- Open a browser window for OAuth authentication
- Ask you to sign in to your Google account
- Authorize the application
- Generate and save `token.json`

## Usage

### Running the Client

The main client connects to both math and Gmail servers:

```bash
python client.py
```

### Available Operations

#### Math Operations
- Basic arithmetic: addition, subtraction, multiplication, division
- Mathematical functions: square root, power, etc.

#### Gmail Operations
- **Send Email**: `send-email` tool
- **Get Unread Emails**: `get-unread-emails` tool
- **Read Email**: `read-email` tool
- **Trash Email**: `trash-email` tool
- **Mark as Read**: `mark-email-as-read` tool
- **Open Email in Browser**: `open-email` tool

### Example Queries

```python
# Send an email
"Send an email to john@example.com with subject 'Meeting Tomorrow' and message 'Let's meet at 2 PM'"

# Check unread emails
"Check my unread emails"

# Read a specific email
"Read email with ID 12345"

# Trash an email
"Move email 12345 to trash"
```

## LangGraph Integration

The project uses LangGraph's StateGraph for managing the tool calling loop:

### State Management
- Uses `TypedDict` with `Annotated` lists for type safety
- Implements `add_messages` reducer for proper message state management
- Maintains conversation history with tool calls and responses

### Graph Structure
- **LLM Node**: Processes user input and generates tool calls
- **Tools Node**: Executes MCP tool calls
- **Loop**: Continues until final response is generated

## Architecture

### MCP Servers
- **Math Server**: Simple mathematical operations
- **Gmail Server**: Full Gmail API integration with OAuth authentication

### Client Architecture
- **MultiServerMCPClient**: Connects to multiple MCP servers
- **LangGraph StateGraph**: Manages conversation flow and tool calling
- **Groq LLM**: Processes natural language and generates tool calls

## Troubleshooting

### Common Issues

1. **Gmail Authentication Error**:
   - Ensure `credentials.json` is in the project root
   - Delete `token.json` and regenerate if expired
   - Check Google Cloud Console API settings

2. **Import Errors**:
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **Tool Not Triggered**:
   - Check that tools are properly bound to the LLM in the graph
   - Verify MCP server connections are active

### Debug Mode

To debug tool messages and LLM responses, the client includes print statements in the LLM node to inspect message history and ToolMessages.

## Dependencies

Key dependencies include:
- `langchain`: Core LangChain functionality
- `langgraph`: StateGraph and message management
- `langchain-mcp-adapters`: MCP server integration
- `langchain-groq`: Groq LLM integration
- `mcp`: MCP protocol implementation
- `google-api-python-client`: Gmail API integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and development purposes. Please ensure compliance with Google's API terms of service when using the Gmail integration.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Google Cloud Console documentation
3. Check MCP and LangChain documentation 
