"""
Text Processing Utilities

Provides various text processing functions, such as emoji removal, text cleaning, etc.
"""
import re

def remove_emojis(text):
    """
    Remove emojis from text
    
    Args:
        text: Input text
        
    Returns:
        Text with emojis removed
    """
    if not text:
        return text
        
    # Unicode ranges for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
        "\U0001FA00-\U0001FA6F"  # Extended Symbols & Pictographs
        "\U0001FA70-\U0001FAFF"  # Extended Symbols & Pictographs
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def clean_text(text):
    """
    Clean text by removing emojis and excess whitespace
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return text
        
    # Remove emojis
    text = remove_emojis(text)
    
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text 