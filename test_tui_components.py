"""
Test script to verify the DeckForge TUI components work correctly
"""
import asyncio
from textual.app import App
from textual.widgets import Label
from tui.app import DeckForgeApp

def test_app_creation():
    """Test that the app can be created without errors."""
    try:
        app = DeckForgeApp()
        print("[SUCCESS] App created successfully")
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    modules_to_test = [
        "tui.app",
        "tui.bridge", 
        "tui.screens.dashboard",
        "tui.screens.forge_builder",
        "tui.screens.investigator",
        "core.schema"
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"[SUCCESS] {module_name} imported successfully")
        except ImportError as e:
            print(f"✗ {module_name} import failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Testing DeckForge TUI components...\n")
    
    success = True
    success &= test_imports()
    success &= test_app_creation()
    
    print(f"\nOverall result: {'[SUCCESS] All tests passed!' if success else '[ERROR] Some tests failed'}")