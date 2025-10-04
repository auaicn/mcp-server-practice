#!/usr/bin/env python3
"""
Basic MCP Server Example
A simple weather information server demonstrating core MCP concepts
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    Prompt,
    PromptMessage,
    GetPromptResult,
)
from mcp.server.stdio import stdio_server

# Initialize MCP server
app = Server("weather-server")

# Sample data for demonstration
WEATHER_DATA = {
    "seoul": {"temp": 18, "condition": "Cloudy", "humidity": 65},
    "tokyo": {"temp": 22, "condition": "Sunny", "humidity": 55},
    "london": {"temp": 12, "condition": "Rainy", "humidity": 80},
}

# 1. List available tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return list of available tools"""
    return [
        Tool(
            name="get_weather",
            description="Get current weather information for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., seoul, tokyo, london)",
                    }
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_forecast",
            description="Get 3-day weather forecast for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name",
                    },
                    "days": {
                        "type": "number",
                        "description": "Number of days (1-3)",
                        "default": 3,
                    }
                },
                "required": ["city"],
            },
        ),
    ]


# 2. Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute tool based on name"""
    
    if name == "get_weather":
        city = arguments.get("city", "").lower()
        
        if city not in WEATHER_DATA:
            return [
                TextContent(
                    type="text",
                    text=f"Weather data not available for {city}. Available cities: {', '.join(WEATHER_DATA.keys())}"
                )
            ]
        
        weather = WEATHER_DATA[city]
        result = f"Weather in {city.title()}:\n"
        result += f"Temperature: {weather['temp']}°C\n"
        result += f"Condition: {weather['condition']}\n"
        result += f"Humidity: {weather['humidity']}%"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_forecast":
        city = arguments.get("city", "").lower()
        days = min(arguments.get("days", 3), 3)
        
        if city not in WEATHER_DATA:
            return [
                TextContent(
                    type="text",
                    text=f"Forecast data not available for {city}"
                )
            ]
        
        result = f"{days}-day forecast for {city.title()}:\n"
        for day in range(1, days + 1):
            result += f"Day {day}: {WEATHER_DATA[city]['condition']}, "
            result += f"{WEATHER_DATA[city]['temp'] + day}°C\n"
        
        return [TextContent(type="text", text=result)]
    
    raise ValueError(f"Unknown tool: {name}")


# 3. List available resources
@app.list_resources()
async def list_resources() -> list[Resource]:
    """Return list of available resources"""
    return [
        Resource(
            uri="weather://cities",
            name="Available Cities",
            mimeType="application/json",
            description="List of cities with weather data",
        ),
        Resource(
            uri=f"weather://city/seoul",
            name="Seoul Weather",
            mimeType="application/json",
            description="Current weather data for Seoul",
        ),
    ]


# 4. Read resource content
@app.read_resource()
async def read_resource(uri: str) -> str:
    """Return resource content based on URI"""
    
    if uri == "weather://cities":
        return json.dumps(list(WEATHER_DATA.keys()), indent=2)
    
    if uri.startswith("weather://city/"):
        city = uri.split("/")[-1].lower()
        if city in WEATHER_DATA:
            return json.dumps(WEATHER_DATA[city], indent=2)
        raise ValueError(f"City not found: {city}")
    
    raise ValueError(f"Unknown resource: {uri}")


# 5. List available prompts
@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """Return list of available prompt templates"""
    return [
        Prompt(
            name="weather_report",
            description="Generate a weather report for a city",
            arguments=[
                {
                    "name": "city",
                    "description": "City name",
                    "required": True,
                }
            ],
        )
    ]


# 6. Get prompt content
@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str]) -> GetPromptResult:
    """Return prompt content based on name and arguments"""
    
    if name == "weather_report":
        city = arguments.get("city", "Seoul")
        
        return GetPromptResult(
            description=f"Weather report prompt for {city}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please provide a detailed weather report for {city}, including temperature, conditions, and any recommendations for outdoor activities."
                    ),
                )
            ],
        )
    
    raise ValueError(f"Unknown prompt: {name}")


# Main entry point
async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())