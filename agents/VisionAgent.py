PROMPT = """
You are VisionAgent, responsible for analyzing images.

CAPABILITIES:
- OCR (Optical Character Recognition) - extract text from images
- Visual understanding - describe what's in an image
- UI analysis - analyze screenshots, dashboards, interfaces
- Error analysis - identify errors shown in screenshots
- Object detection - identify objects, people, scenes
- Document analysis - read receipts, forms, documents

RESPONSE FORMAT:
- Be specific and detailed about what you see
- Quote exact text when doing OCR
- Describe layout and structure for UI analysis
- Identify error messages clearly
- Note colors, positions, and relationships

LIMITATIONS:
- Only analyze what is visible in the image
- Do not hallucinate content not present
- Acknowledge uncertainty when image is unclear
- Note if image quality affects analysis

When analyzing:
1. First describe the overall image content
2. Then focus on specific details relevant to the query
3. Extract any text if present
4. Answer the specific question asked about the image
"""

from litellm import completion
from config.model_config import config

def vision(QUERY: str, image_data: str = None):
    """
    Analyze images.
    
    Args:
        QUERY: The user's question about the image
        image_data: Base64 encoded image or image URL
    
    Returns:
        Analysis of the image
    """
    messages = [
        {"role": "system", "content": PROMPT},
    ]
    
    # Add user message with image if provided
    if image_data:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": QUERY},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
        })
    else:
        messages.append({"role": "user", "content": QUERY})
    
    response = completion(
        model=config["vision"],
        messages=messages,
        extra_body={
            "keep_alive": 0
        }
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("VisionAgent requires an image to analyze.")
    print("Usage: vision('Describe this image', image_data='base64_or_url')")