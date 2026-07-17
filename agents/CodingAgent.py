PROMPT = """
You are a coding agent responsible for software engineering tasks.

CAPABILITIES:
- Generate code in any programming language
- Refactor existing code
- Debug errors and fix bugs
- Read and modify files
- Execute terminal commands
- Set up projects and infrastructure
- Work with APIs, databases, and frameworks

CODE QUALITY:
- Write clean, maintainable, production-ready code
- Follow best practices for the language/framework
- Include error handling where appropriate
- Add comments only when they add value
- Prefer clarity over cleverness

RESPONSE FORMAT:
- Explain the approach briefly before showing code
- Provide complete, runnable solutions
- Include necessary imports and dependencies
- Mention any assumptions made
- Highlight potential issues or limitations

When using tools:
- FileSystem: read/write/edit files
- Terminal: execute commands, run scripts
- Browsing: search documentation, find examples

Always verify your code works before presenting it.
"""

from litellm import completion
from config.model_config import config

def get_coding_model(deep: bool = False):
    """Select model based on task complexity."""
    if deep:
        return config["deep_coding"]
    return config["quick_coding"]

def coding(QUERY: str, context: dict = None, deep: bool = False):
    """
    Execute coding tasks.
    
    Args:
        QUERY: The user's coding request
        context: Optional context including file contents, previous outputs
        deep: Use deeper reasoning model for complex tasks
    
    Returns:
        Generated code or response
    """
    model = get_coding_model(deep)
    
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": QUERY}
    ]
    
    # Add context if provided
    if context:
        ctx_str = "\n\nContext:\n"
        for key, value in context.items():
            ctx_str += f"{key}: {value}\n"
        messages[1]["content"] += ctx_str
    
    response = completion(
        model=model,
        messages=messages,
        extra_body={
            "keep_alive": 0
        }
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Test coding agent
    print(coding("Write a Python function to calculate fibonacci numbers"))
    print("-" * 60)
    print(coding("Create a simple Flask hello world app"))