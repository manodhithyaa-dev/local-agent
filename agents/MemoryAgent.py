PROMPT = """
You are MemoryAgent, responsible for extracting and storing information about the user.

OBJECTIVE:
- Extract relevant facts, preferences, interests, and skills from conversations
- Update the user's profile and memory files
- Build a long-term understanding of the user over time
- Store only useful, lasting information - not every detail

MEMORY CATEGORIES:

1. facts (facts.md):
   - Objective information about the user
   - Hardware, software, OS, location
   - Technical specifications
   - Verifiable facts
   Example: "User uses Ubuntu 24.04", "User has RTX 4050 GPU"

2. profile (profile.md):
   - Identity and background
   - Role, profession, education
   - Personal preferences
   - Working style
   Example: "Computer Science student", "Prefers minimal setups"

3. interest (interest.md):
   - Long-term interests and hobbies
   - Technologies they want to learn
   - Project domains they care about
   Example: "Interested in AI agents", "Learning robotics"

4. skills (skills.md):
   - Learned workflows and preferences
   - Coding patterns they prefer
   - Tool preferences
   - Best practices they follow
   Example: "Prefers FastAPI over Flask", "Uses type hints in Python"

5. chat (chat.md):
   - Important conversation summaries
   - Project context that may be referenced later
   - Decisions made together
   - Not every message - only useful context

EXTRACTION RULES:
- Extract information explicitly stated or clearly implied
- Do not infer beyond what is reasonable
- Prioritize recent information over old
- Merge duplicate information
- Remove outdated information when contradicted
- Be concise but specific

OUTPUT FORMAT:
Return a JSON object with updates for each category:
{
    "facts": ["new fact 1", "new fact 2"],
    "profile": ["new profile item"],
    "interest": ["new interest"],
    "skills": ["new skill/preference"],
    "chat_summary": "brief summary if conversation should be stored"
}

Only include categories that have new information to add.
Empty arrays mean no update needed for that category.
"""

from litellm import completion
import json
import re
import os
from datetime import datetime
from config.model_config import config

MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory")

def extract_memory(QUERY: str, response: str):
    """
    Extract memory-worthy information from a conversation.
    
    Args:
        QUERY: User's query
        response: Agent's response
    
    Returns:
        dict with memory updates by category
    """
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"User: {QUERY}\n\nAssistant: {response}"}
    ]
    
    response = completion(
        model=config["chat"],  # Use chat model for memory extraction
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
        return {}

def read_memory_file(category: str) -> str:
    """Read a memory file's contents."""
    path = os.path.join(MEMORY_DIR, category, f"{category}.md")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def write_memory_file(category: str, content: str):
    """Write content to a memory file."""
    path = os.path.join(MEMORY_DIR, category, f"{category}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def append_to_memory(category: str, items: list):
    """Append new items to a memory file."""
    if not items:
        return
    
    current = read_memory_file(category)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Add new items with timestamp
    for item in items:
        if item.strip():
            current += f"\n- [{timestamp}] {item.strip()}"
    
    write_memory_file(category, current)

def update_chat_summary(summary: str):
    """Add a conversation summary to chat memory."""
    if not summary:
        return
    
    current = read_memory_file("chat")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"\n\n## {timestamp}\n{summary.strip()}\n"
    current += entry
    
    write_memory_file("chat", current)

def process_memory(QUERY: str, response: str):
    """
    Full memory processing pipeline.
    
    Args:
        QUERY: User's query
        response: Agent's response
    """
    # Extract memory items
    memory_updates = extract_memory(QUERY, response)
    
    # Apply updates
    for category in ["facts", "profile", "interest", "skills"]:
        if category in memory_updates and memory_updates[category]:
            append_to_memory(category, memory_updates[category])
    
    if "chat_summary" in memory_updates and memory_updates["chat_summary"]:
        update_chat_summary(memory_updates["chat_summary"])
    
    return memory_updates

if __name__ == "__main__":
    # Test memory agent
    test_query = "I'm building an AI agent system with LangChain on my Ubuntu laptop with RTX 4050"
    test_response = "That sounds like a great project! With your RTX 4050, you can run 7B models locally..."
    
    print("Processing memory...")
    result = process_memory(test_query, test_response)
    print(json.dumps(result, indent=2))
    
    print("\nMemory files updated:")
    for category in ["facts", "profile", "interest", "skills", "chat"]:
        content = read_memory_file(category)
        if content:
            print(f"\n{category}/:")
            print(content[:200] + "..." if len(content) > 200 else content)