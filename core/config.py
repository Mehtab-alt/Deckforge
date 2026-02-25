import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class DeckForgeConfig:
    """Configuration class for DeckForge application."""
    
    # API Keys and Authentication
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    
    # Application Settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    knowledge_base_path: str = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base")
    exports_path: str = os.getenv("EXPORTS_PATH", "exports")
    templates_path: str = os.getenv("TEMPLATES_PATH", "templates")
    
    # LLM Settings
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4-turbo")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0"))
    
    # Vector Database Settings
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./storage/chroma_db")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Terraform Settings
    terraform_binary: str = os.getenv("TERRAFORM_BINARY", "terraform")
    
    def validate(self) -> None:
        """Validate the configuration."""
        errors = []
        
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required")
            
        if not self.github_token and os.getenv("GITHUB_TOKEN_REQUIRED", "false").lower() == "true":
            errors.append("GITHUB_TOKEN is required")
            
        if not os.path.exists(self.knowledge_base_path):
            errors.append(f"Knowledge base path does not exist: {self.knowledge_base_path}")
            
        if errors:
            raise ValueError("Configuration validation failed: " + "; ".join(errors))