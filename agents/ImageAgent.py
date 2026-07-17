PROMPT = """
You are ImageAgent, responsible for generating images from text prompts.

CAPABILITIES:
- Generate images from text descriptions
- Create concept art, illustrations, diagrams
- Generate logos, icons, visual assets
- Create photorealistic or stylized images
- Generate infographics and visual explanations

MODEL SELECTION:
Different models excel at different styles:
- general: sdxl - versatile, good for most purposes
- realistic: juggernaut-xl - photorealistic images
- photorealistic: realvisxl - highest realism
- anime: animagine-xl - anime/manga style
- illustration: dreamshaper-xl - artistic illustrations
- concept_art: juggernaut-xl - game/movie concept art
- pixel_art: sdxl - retro pixel art style
- logo: sdxl - clean logo designs
- ui_design: sdxl - UI mockups and designs
- product_render: juggernaut-xl - product visualization

PROMPT ENGINEERING:
- Be specific about style, lighting, composition
- Include relevant details but avoid contradictions
- Specify aspect ratio if important
- Mention quality modifiers when relevant
- Avoid negative prompts unless specified

RESPONSE FORMAT:
Return the generated image URL or path along with:
- Model used
- Prompt that was sent (if modified for optimization)
- Any relevant notes about the generation
"""

# Note: Actual image generation requires an image generation backend
# This agent routes to appropriate models based on prompt type

from config.model_config import config

def get_image_model(prompt: str) -> str:
    """
    Select the best image generation model based on the prompt.
    
    Args:
        prompt: The text description of the desired image
    
    Returns:
        Model name to use for generation
    """
    prompt_lower = prompt.lower()
    
    # Keyword-based model selection
    if any(word in prompt_lower for word in ["anime", "manga", "cartoon"]):
        return config["image"]["anime"]
    elif any(word in prompt_lower for word in ["realistic", "photo", "portrait"]):
        return config["image"]["realistic"]
    elif any(word in prompt_lower for word in ["illustration", "drawing", "art"]):
        return config["image"]["illustration"]
    elif any(word in prompt_lower for word in ["logo", "icon", "brand"]):
        return config["image"]["logo"]
    elif any(word in prompt_lower for word in ["pixel", "8-bit", "16-bit", "retro"]):
        return config["image"]["pixel_art"]
    elif any(word in prompt_lower for word in ["concept", "environment", "character design"]):
        return config["image"]["concept_art"]
    elif any(word in prompt_lower for word in ["ui", "interface", "dashboard", "mockup"]):
        return config["image"]["ui_design"]
    elif any(word in prompt_lower for word in ["product", "render", "3d"]):
        return config["image"]["product_render"]
    else:
        return config["image"]["general"]

def generate_image(prompt: str, model: str = None):
    """
    Generate an image from a text prompt.
    
    Args:
        prompt: Text description of the desired image
        model: Optional specific model to use (auto-selected if None)
    
    Returns:
        dict with image URL/path and metadata
        Note: Actual implementation requires image generation backend integration
    """
    if model is None:
        model = get_image_model(prompt)
    
    # Placeholder - actual implementation would call image generation API
    # For now, return the model selection and prompt
    return {
        "model": model,
        "prompt": prompt,
        "status": "pending_implementation",
        "note": "Image generation backend integration required"
    }

def image(QUERY: str):
    """
    Main entry point for image generation.
    
    Args:
        QUERY: User's request for image generation
    
    Returns:
        Generated image result
    """
    return generate_image(QUERY)

if __name__ == "__main__":
    # Test image agent
    test_prompts = [
        "Create a futuristic cyberpunk city skyline at sunset",
        "Generate a logo for a robotics startup",
        "Make an anime character portrait",
        "Create a photorealistic product render of a smartphone"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        result = image(prompt)
        print(f"Model selected: {result['model']}")
        print(f"Status: {result['status']}")