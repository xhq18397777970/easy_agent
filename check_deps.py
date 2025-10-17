#!/usr/bin/env python3

try:
    import whois
    print("✅ whois module is available")
except ImportError as e:
    print(f"❌ whois module not found: {e}")

try:
    import mcp
    print("✅ mcp module is available")
except ImportError as e:
    print(f"❌ mcp module not found: {e}")

try:
    from mcp.server.fastmcp import FastMCP
    print("✅ FastMCP is available")
except ImportError as e:
    print(f"❌ FastMCP not found: {e}")