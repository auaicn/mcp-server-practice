# MCP Server Practice

This project is dedicated to learning and practicing with Model Context Protocol (MCP) servers. MCP is a standardized protocol that enables AI assistants to connect securely to data sources and tools.

## Overview

This practice project will help you understand and implement various aspects of MCP servers, including:

- Understanding the MCP protocol and architecture
- Creating custom MCP servers
- Implementing different types of tools and resources
- Working with prompts and completions
- Error handling and debugging
- Testing and deployment strategies

## Getting Started

To begin practicing with MCP servers, you'll need:

1. Familiarity with the MCP specification
2. A development environment set up
3. Basic understanding of JSON-RPC protocols
4. Knowledge of the programming language you'll be using

### Requirements


- python 3.12 (or higher)
  - to use mcp, python 3.12 or higher version is required.
  - see also this file. [pyproject.toml](pyproject.toml)

## venv

### make venv

```
python3 -m venv .venv
```

### enable python virtial env

```
source .venv/bin/activate
```
 
shell 영역에 (venv) 가 보이는 것을 확인하자. 

### disable python virtual env

```
deactivate
```

### requirements.txt

after enabling python virtual env, use this command

```
pip install -r requirements.txt
```

if you have changes about package dependencies, you may update requirements.txt using

```
pip freeze > requirements.txt
```

## Project Structure

This repository will contain various MCP server implementations and examples as you progress through your learning journey.

### FAQS

- (case of Apple Silicon MacOS) claude logs are located under 

```
~/Library/Logs/Claude
```

## Resources

- [Official MCP Documentation](https://modelcontextprotocol.io/)
  - [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## Practice Areas

- **Basic Server Setup**: Creating your first MCP server
- **Tool Implementation**: Adding tools that the client can invoke
- **Resource Handling**: Serving structured data
- **Prompt Engineering**: Implementing prompt templates
- **Error Handling**: Proper error responses and debugging
- **Authentication**: Secure server implementations
- **Testing**: Unit and integration tests for MCP servers

Happy coding!
