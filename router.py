from agents.ChatAgent import chat
from agents.ClassifierAgent import ClassifierAgent
from agents.LogicalAgent import logical
from agents.PlannerAgent import planner

import json

def router(QUERY):
    route = ClassifierAgent(QUERY)
    
    return route

if __name__ == "__main__":
    test_queries = [
        # Chat
        "Why do airplanes leave white trails in the sky?",
        "Explain blockchain like I'm 12 years old.",
        "What causes seasons on Earth?",
        "Tell me an interesting fact about octopuses.",

        # Logical
        "I have $5,000 to invest. Compare index funds, bonds, and gold for a 10-year horizon.",
        "Analyze the pros and cons of remote work versus office work.",
        "I need to choose between buying a car or using ride-sharing. Help me decide.",
        "A train leaves Chennai at 8 AM and another leaves Bangalore at 9 AM. When will they meet?",

        # Coding
        "Create a FastAPI service with JWT authentication and role-based access control.",
        "Refactor this JavaScript function to improve performance.",
        "Write a Bash script that automatically backs up my project folder.",
        "Debug why my Docker container keeps restarting.",

        # Coding + Planning
        "Build a complete inventory management system with frontend, backend, and database.",
        "Design a scalable microservice architecture for an e-commerce platform.",
        "Create a CI/CD workflow that deploys to AWS when code is pushed to main.",
        "Migrate a monolithic Laravel application into separate services.",

        # Terminal / Filesystem
        "Delete every .tmp file inside the current project directory.",
        "Find all files larger than 500MB on my machine.",
        "Move the logs folder into an archive directory and compress it.",
        "List every Python file and count their lines of code.",

        # Memory Required
        "Continue the project architecture we discussed yesterday.",
        "Use the tech stack I normally prefer.",
        "Remind me what database I usually choose for my projects.",
        "Generate code that follows my standard folder structure.",

        # Image Generation
        "Create a futuristic cyberpunk city skyline at sunset.",
        "Generate a logo for a robotics startup called Nova Robotics.",
        "Make an infographic explaining how neural networks learn.",
        "Draw a fantasy map with mountains, rivers, and kingdoms.",

        # Vision (assuming image attached)
        "[image attached] Extract all text visible in this receipt.",
        "[image attached] Identify the error shown in this screenshot.",
        "[image attached] Describe the layout of this dashboard UI.",
        "[image attached] What objects are visible in this photo?",

        # Ambiguous
        "Do it again.",
        "Make it better.",
        "Continue.",
        "Fix everything.",

        # Research
        "Research the latest developments in quantum computing and summarize them.",
        "Find recent trends in autonomous robotics and explain their impact.",
        "Investigate current AI agent frameworks and compare their approaches.",
        "Summarize recent cybersecurity threats affecting Linux servers.",

        # Mixed Cases
        "Analyze this system design and then generate an improved architecture diagram.",
        "Read the screenshot and create a cleaner UI mockup.",
        "Compare PostgreSQL and MongoDB, then recommend one for my application.",
        "Review my deployment strategy and suggest improvements."
    ]

    for query in test_queries:
        print(f"\n> {query}")
        print(json.dumps(router(query), indent=4))
        