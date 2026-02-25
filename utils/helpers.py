import os
import json
import base64
from typing import Dict, Any, Optional
from pathlib import Path


def save_artifacts_to_disk(artifacts: Dict[str, str], project_path: str) -> None:
    """
    Save generated artifacts to disk in the specified project path.
    
    Args:
        artifacts: Dictionary mapping file paths to their content
        project_path: Base directory to save artifacts in
    """
    project_dir = Path(project_path)
    project_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path, content in artifacts.items():
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load and return the content of a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON content or None if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def encode_image_to_base64(image_path: str) -> Optional[str]:
    """
    Encode an image file to base64 string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image or None if file doesn't exist
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except OSError:
        return False


def read_file_contents(file_path: str) -> Optional[str]:
    """
    Read and return the contents of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File contents as string or None if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file_contents(file_path: str, content: str) -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
        
    Returns:
        True if write was successful
    """
    try:
        # Create parent directories if they don't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except OSError:
        return False