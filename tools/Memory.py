"""
Memory Tool - Search and retrieve from the LLM Wiki (user memory).
"""

import os
from pathlib import Path
from typing import List, Optional, Dict

MEMORY_DIR = Path("/workspace/memory")

def search_memory(query: str, categories: List[str] = None) -> Dict:
    """
    Search across memory files for relevant information.
    
    Args:
        query: What to search for
        categories: Specific categories to search (facts, profile, interest, skills, chat)
                   If None, searches all categories
    
    Returns:
        dict with matches from each category
    """
    if categories is None:
        categories = ["facts", "profile", "interest", "skills", "chat"]
    
    results = {}
    query_lower = query.lower()
    
    for category in categories:
        content = read_category(category)
        if not content:
            continue
        
        # Simple keyword matching - could be enhanced with embeddings
        lines = content.split("\n")
        matches = []
        
        for line in lines:
            if any(word in line.lower() for word in query_lower.split()):
                matches.append(line.strip())
        
        if matches:
            results[category] = matches[:10]  # Limit to top 10 matches per category
    
    return {
        "query": query,
        "results": results,
        "note": "Simple keyword search. Consider implementing semantic search with embeddings."
    }

def read_category(category: str) -> Optional[str]:
    """
    Read a memory category file.
    
    Args:
        category: One of facts, profile, interest, skills, chat
    
    Returns:
        File contents or None if not found/empty
    """
    path = MEMORY_DIR / category / f"{category}.md"
    
    if not path.exists():
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    return content if content else None

def get_facts() -> str:
    """Get all stored facts about the user."""
    return read_category("facts") or "No facts stored yet."

def get_profile() -> str:
    """Get user profile information."""
    return read_category("profile") or "No profile information stored yet."

def get_interests() -> str:
    """Get user interests."""
    return read_category("interest") or "No interests stored yet."

def get_skills() -> str:
    """Get learned skills and preferences."""
    return read_category("skills") or "No skills/preferences stored yet."

def get_chat_history() -> str:
    """Get conversation summaries."""
    return read_category("chat") or "No chat history stored yet."

def get_context_for_query(query: str) -> str:
    """
    Get relevant memory context for a query.
    Useful for providing context to agents before they respond.
    
    Args:
        query: The user's query
    
    Returns:
        Formatted string with relevant memory context
    """
    search_results = search_memory(query)
    
    if not search_results["results"]:
        return "No relevant memory found."
    
    context_parts = []
    for category, matches in search_results["results"].items():
        context_parts.append(f"\n## {category.capitalize()}")
        for match in matches:
            context_parts.append(f"- {match}")
    
    return "\n".join(context_parts)

if __name__ == "__main__":
    # Test Memory tool
    print("Testing Memory Tool...\n")
    
    # Show current memory state
    print("=== Current Memory State ===\n")
    
    print("Facts:")
    print(get_facts())
    print("\nProfile:")
    print(get_profile())
    print("\nInterests:")
    print(get_interests())
    print("\nSkills:")
    print(get_skills())
    print("\nChat History:")
    print(get_chat_history())
    
    # Test search
    print("\n\n=== Search Test ===")
    results = search_memory("AI agent")
    print(f"\nSearch for 'AI agent':")
    print(results)