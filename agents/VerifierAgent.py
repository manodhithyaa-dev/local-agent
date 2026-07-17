PROMPT = """
You are VerifierAgent, responsible for reviewing agent output before it reaches the user.

OBJECTIVE:
- Check correctness, completeness, security, logic, and code quality
- Approve output or request revision
- Catch errors, bugs, security issues, and logical flaws

VERIFICATION CHECKLIST:

For Code:
- Syntax correctness
- Logic correctness
- Error handling
- Security vulnerabilities (injection, XSS, auth issues)
- Edge cases
- Performance concerns
- Best practices adherence
- Completeness (does it solve the full problem?)

For Reasoning/Analysis:
- Logical consistency
- Factual accuracy
- Complete coverage of the question
- Sound assumptions
- Valid conclusions

For General Responses:
- Accuracy of information
- Completeness
- Clarity
- Relevance to the query

RESPONSE FORMAT:
Return a JSON object with:
{
    "approved": true/false,
    "issues": ["list of issues found"],
    "suggestions": ["list of improvement suggestions"],
    "revision_request": "explanation if revision needed"
}

If approved, issues and suggestions can be empty.
If not approved, clearly explain what needs revision.

CRITICAL RULES:
- Be thorough but pragmatic
- Flag security issues immediately
- Don't approve incomplete solutions
- Don't approve code with obvious bugs
- Request revision when quality is insufficient
"""

from litellm import completion
import json
import re
from config.model_config import config

def verify(output: str, query: str, agent_type: str = "general"):
    """
    Verify agent output before presenting to user.
    
    Args:
        output: The generated response to verify
        query: Original user query for context
        agent_type: Type of agent that generated this (coding, logical, chat, etc.)
    
    Returns:
        dict with approval status and feedback
    """
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"Query: {query}\n\nOutput to verify:\n{output}"}
    ]
    
    response = completion(
        model=config["verifier"],
        messages=messages,
        extra_body={
            "keep_alive": 0
        }
    )
    
    raw = response.choices[0].message.content
    
    # Clean markdown if present
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback if parsing fails
        return {
            "approved": False,
            "issues": ["Failed to parse verification response"],
            "suggestions": [],
            "revision_request": "Verification failed to produce valid JSON"
        }

if __name__ == "__main__":
    # Test verifier
    test_code = '''
def divide(a, b):
    return a / b
'''
    
    result = verify(test_code, "Write a division function", "coding")
    print(json.dumps(result, indent=2))