# MCP server + client weather example

## Setup

### 1. Create a virtual environment and install the dependencies:
```bash
uv sync
```

### 2. Create a `.env` file for your Anthropic API key:
```bash
echo "ANTHROPIC_API_KEY=your-api-key-goes-here" > .env
```

## Running the example client

Run the server and client using the following command:
```bash
uv run client.py ./server.py
```

## Use with other clients

### VS Code
Add the following to your `.vscode/mcp.json` file to use this server in VS Code:
```json
{
	"servers": {
		"weather": {
			"type": "stdio",
			"command": "uv",
			"args": [
				"--directory",
				"/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
				"run",
				"weather.py"
			]
		}
	},
	"inputs": []
}
```

## References
- [Build an MCP Server](https://modelcontextprotocol.io/docs/develop/build-server)
- [Build an MCP Client](https://modelcontextprotocol.io/docs/develop/build-client)