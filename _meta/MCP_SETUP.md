# MCP Server Setup Guide

## Overview

This document covers setup for two MCP servers:
1. **google-scholar-mcp** - Search Google Scholar from Claude Code
2. **zotero-mcp** - Connect your Zotero library to Claude Code

---

## 1. Google Scholar MCP Setup

### Option A: Automated Installation (Easiest)

**Requirements:**
- Node.js installed

**Installation:**
```bash
npx -y @smithery/cli install @mochow13/google-scholar-mcp --client claude
```

This automatically configures Claude Desktop to use the server.

### Option B: Manual Installation

**Requirements:**
- Node.js 14+ and npm

**Steps:**
```bash
# Clone the repository
git clone https://github.com/mochow13/google-scholar-mcp.git
cd google-scholar-mcp

# Install dependencies in server directory
cd server
npm install
npm run build

# Install dependencies in client directory (if using standalone client)
cd ../client
npm install
npm run build

# Start the server
cd ../server
node build/index.js
```

### Configuration for Claude Code

Add to your Claude Code configuration (or Claude Desktop if using that):

```json
{
  "mcpServers": {
    "google-scholar": {
      "command": "node",
      "args": ["/path/to/google-scholar-mcp/server/build/index.js"]
    }
  }
}
```

### Features
- Search Google Scholar papers by keyword
- Get paper metadata (title, authors, year, citation count)
- Access abstract and availability information
- Filter results by publication year and other criteria

---

## 2. Zotero MCP Setup

### Requirements

**System Requirements:**
- Python 3.10 or higher
- Zotero 7+ (desktop application)
- MCP-compatible client (Claude Code/Claude Desktop)

**Python Setup Check:**
```bash
python --version  # Should be 3.10 or higher
```

### Option A: Automated Installation with uv (Recommended)

**Install uv if you don't have it:**
```bash
pip install uv
```

**Then install zotero-mcp:**
```bash
uv tool install "git+https://github.com/54yyyu/zotero-mcp.git"
zotero-mcp setup
```

### Option B: Installation with pip

```bash
pip install git+https://github.com/54yyyu/zotero-mcp.git
zotero-mcp setup
```

### Option C: Automated Installation with Smithery

```bash
npx -y @smithery/cli install @54yyyu/zotero-mcp --client claude
```

### Configuration Steps

#### 1. Enable Zotero Local API

1. Open **Zotero Desktop** application
2. Go to **Edit** → **Preferences** (Windows/Linux) or **Zotero** → **Preferences** (Mac)
3. Navigate to **Advanced** tab
4. Check the box: **"Enable local API"**
5. Take note of the API key shown (you may need it for configuration)
6. Restart Zotero

#### 2. Run Setup

```bash
zotero-mcp setup
```

This will:
- Detect your Zotero installation
- Configure embedding models (optional, for semantic search)
- Add server to your MCP client configuration automatically

#### 3. Optional: Configure Semantic Search

```bash
zotero-mcp setup --semantic-config-only
```

Choose your embedding model:
- **Default**: Simple local embeddings
- **OpenAI**: Requires OpenAI API key
- **Gemini**: Requires Google Gemini API key

### Features
- Search your Zotero library by keyword
- Semantic search across papers (with embeddings)
- Get paper summaries and metadata
- Access PDF annotations and highlights
- Analyze citation networks
- Get related papers

---

## Integration with Claude Code

Both servers will be automatically available in Claude Code once installed. You can:

1. **Ask Claude to search** for papers directly in conversations
2. **Import search results** into your project
3. **Analyze and summarize** academic papers
4. **Combine searches** (e.g., "Search Google Scholar for X, then compare with my Zotero library")

---

## Troubleshooting

### Google Scholar MCP
- **"Module not found"**: Run `npm install` and `npm run build` in both directories
- **Port 3000 in use**: Modify the port in server configuration
- **No results**: Check your internet connection and Google Scholar availability

### Zotero MCP
- **"Zotero not found"**: Ensure Zotero 7+ is installed and local API is enabled
- **"Python version error"**: Use `python3.10` or higher
- **Configuration not working**: Delete `~/.config/zotero-mcp/config.json` and rerun `zotero-mcp setup`
- **Permission denied**: On Linux/Mac, you may need to use `sudo` or adjust directory permissions

---

## After Setup

Once both servers are installed:

1. **Restart Claude Code** or **Claude Desktop**
2. In a conversation, you can now:
   - "Search Google Scholar for papers on economic history"
   - "Find papers in my Zotero library about Malthusian economics"
   - "Compare this paper with similar work in my library"

3. Use the tools in your Python notebooks:
   - Import search results
   - Cite papers in your notes
   - Download and analyze paper metadata

---

## Configuration Files

### Claude Desktop Config Location

**Windows:**
```
%APPDATA%/Claude/claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Claude Code Config

For Claude Code CLI, configuration is typically in:
```
~/.claude-code/config.json
```

---

## Next Steps

1. Choose your installation method (automated recommended)
2. Follow the installation steps for each server
3. Run the setup scripts
4. Restart your Claude client
5. Test by asking Claude to search for papers

Questions or issues? Refer to the GitHub repositories:
- [google-scholar-mcp](https://github.com/mochow13/google-scholar-mcp)
- [zotero-mcp](https://github.com/54yyyu/zotero-mcp)
