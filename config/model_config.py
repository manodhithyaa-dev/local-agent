"""
Available Models
NAME                      ID              SIZE
qwen2.5vl:7b              5ced39dfa4ba    06.0 GB
deepseek-r1:7b            755ced02ce7b    04.7 GB
qwen2.5-coder:7b          dae161e27b0e    04.7 GB
qwen3-coder:latest        06c1097efce0    18.0 GB
qwen3:4b                  359d7dd4bcda    02.5 GB
gemma3:4b                 a2af6cc3eb7f    03.3 GB
qwen3:8b                  500a1f067a9f    05.2 GB
llama3.2-vision:latest    6f2f9757ae97    07.8 GB

"""

config = {
    # Core Conversation
    "chat": "ollama/qwen3:8b",
    "logical": "ollama/deepseek-r1:7b",
    "planner": "ollama/qwen3:30b",

    # Coding
    "quick_coding": "ollama/qwen2.5-coder:7b",
    "deep_coding": "ollama/qwen3-coder:latest",
    "verifier": "ollama/qwen2.5-coder:7b",

    # Vision
    "vision": "ollama/qwen2.5vl:7b",

    # Image Generation Router
    "image": {
        "general": "sdxl",
        "realistic": "juggernaut-xl",
        "photorealistic": "realvisxl",
        "anime": "animagine-xl",
        "illustration": "dreamshaper-xl",
        "concept_art": "juggernaut-xl",
        "pixel_art": "sdxl",
        "logo": "sdxl",
        "ui_design": "sdxl",
        "product_render": "juggernaut-xl"
    }
}