#!/usr/bin/env python3
"""
Example usage of the Machine Dialect Runner API.
"""

import requests
import json

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"


def test_api_connection():
    """Test basic API connectivity."""
    print("🔍 Testing API connection...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_health_check():
    """Test health check endpoint."""
    print("🏥 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def execute_code(code, debug=False, description=""):
    """Execute Machine Dialect code and print results."""
    print(f"⚡ {description}")
    print(f"Code:\n{code}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"code": code, "debug": debug}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    print("-" * 50)
    print()


def main():
    """Run example API calls."""
    print("🚀 Machine Dialect Runner API Examples\n")
    
    # Test basic connectivity
    test_api_connection()
    test_health_check()
    
    # Example 1: Simple variable assignment
    execute_code(
        code="""Define `x` as number.
Set `x` to _42_.""",
        description="Example 1: Simple variable assignment"
    )
    
    # Example 2: Basic arithmetic
    execute_code(
        code="""Define `a` as number.
Define `b` as number.
Define `result` as number.
Set `a` to _10_.
Set `b` to _5_.
Set `result` to `a` + `b`.""",
        description="Example 2: Basic arithmetic"
    )
    
    # Example 3: With debug mode
    execute_code(
        code="""Define `temperature` as number.
Set `temperature` to _25_.""",
        debug=True,
        description="Example 3: With debug mode enabled"
    )
    
    # Example 4: Error handling - invalid syntax
    execute_code(
        code="This is not valid Machine Dialect code!",
        description="Example 4: Error handling - invalid syntax"
    )
    
    # Example 5: Error handling - undefined variable
    execute_code(
        code="Set `undefined_var` to _123_.",
        description="Example 5: Error handling - undefined variable"
    )


if __name__ == "__main__":
    main()