#!/usr/bin/env python3
"""
DeckForge Textual Interface
Main entry point for the TUI application
"""

import os
import sys
from tui.app import DeckForgeApp

def main():
    """Main entry point for the DeckForge TUI."""
    # Set environment variables if not already set
    os.environ.setdefault("API_URL", "http://localhost:8000")
    os.environ.setdefault("API_KEY", "dummy-key")
    
    # Create and run the application
    app = DeckForgeApp()
    
    # Run the application
    app.run()

if __name__ == "__main__":
    main()