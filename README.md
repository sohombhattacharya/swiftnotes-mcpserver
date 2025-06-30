# SwiftNotes MCP Server

A Model Context Protocol (MCP) server that provides deep research capabilities by analyzing YouTube videos using the SwiftNotes API. This server enables LLMs to perform comprehensive research by searching, analyzing, and synthesizing insights from multiple YouTube video sources with timestamped citations.

## Features

- **Deep Research Tool**: Comprehensive research on any topic by analyzing multiple YouTube videos
- **Timestamped Citations**: Inline citations with specific timestamps for verification
- **Multi-Source Analysis**: Synthesizes insights from multiple video sources
- **Comprehensive Coverage**: Ideal for news, reviews, educational content, technology trends, and more
- **MCP Protocol Compliance**: Fully compliant with the Model Context Protocol standard

## Installation

### Prerequisites
- Python 3.13 or higher
- SwiftNotes API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd swiftnotes-mcpserver
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```bash
   SWIFTNOTES_API_KEY=your_api_key_here
   ```

   Or set the environment variable directly:
   ```bash
   export SWIFTNOTES_API_KEY=your_api_key_here
   ```

## Usage

### Running the Server

```bash
python server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Available Tools

#### `deep_research`

Performs comprehensive research by analyzing multiple YouTube videos on a topic.

**Parameters:**
- `search_query` (string): The research topic or question to investigate

**Returns:**
- `title`: The title of the generated research report
- `content`: The main content of the report in Markdown format with inline timestamped citations
- `sources`: Array of source objects with number, title, and URL

**Example Usage:**
```python
await deep_research("latest developments in artificial intelligence")
```

## Configuration

### Environment Variables

- `SWIFTNOTES_API_KEY`: Your SwiftNotes API key (required)

### API Settings

- **Base URL**: `https://api.swiftnotes.ai`
- **Timeout**: 300 seconds (5 minutes)

## Error Handling

The server handles various error conditions:

- **Authentication Errors**: Invalid API key
- **Rate Limiting**: Credit limit reached
- **Bad Requests**: Invalid search queries
- **Network Errors**: Connection timeouts and request failures

## MCP Client Integration

This server is designed to work with MCP-compatible clients. Configure your MCP client to use this server by pointing it to the server executable.

### Example MCP Client Configuration

```json
{
  "name": "swiftnotes-research",
  "command": "python",
  "args": ["path/to/server.py"],
  "env": {
    "SWIFTNOTES_API_KEY": "your_api_key_here"
  }
}
```

## Development

### Project Structure

```
swiftnotesmcpserver/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
├── pyproject.toml     # Project configuration
├── .env               # Environment variables (create this)
├── .python-version    # Python version specification
└── README.md          # This file
```

### Dependencies

Key dependencies include:
- `fastmcp`: FastMCP framework for MCP protocol implementation
- `httpx`: HTTP client for API calls
- `python-dotenv`: Environment variable management

## API Reference

### SwiftNotes API

This server integrates with the SwiftNotes API to perform deep research. The API provides:

- Video search and analysis
- Transcript processing
- Content synthesis
- Source attribution with timestamps

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues related to:
- **MCP Server**: Open an issue in this repository
- **SwiftNotes API**: Contact SwiftNotes support

## Changelog

### v0.1.0
- Initial release
- Deep research tool implementation
- MCP protocol compliance
- SwiftNotes API integration
