"""
Test script to verify the DeckForge TUI structure is correct
"""
from textual.app import App
from textual.widgets import Header, Footer, ContentSwitcher
from tui.app import DeckForgeApp
from tui.screens.dashboard import Dashboard
from tui.screens.forge_builder import ForgeBuilder
from tui.screens.investigator import InvestigatorScreen

def test_app_structure():
    """Test that the app structure is correct."""
    print("Testing DeckForge TUI structure...")
    
    app = DeckForgeApp()
    
    # Test that app has required attributes
    assert hasattr(app, 'TITLE'), "App should have TITLE attribute"
    assert hasattr(app, 'BINDINGS'), "App should have BINDINGS attribute"
    assert hasattr(app, 'metrics'), "App should have metrics reactive attribute"
    assert hasattr(app, 'connection_status'), "App should have connection_status reactive attribute"
    assert hasattr(app, 'api'), "App should have api attribute"
    
    print("[SUCCESS] App has all required attributes")
    
    # Test that screens can be instantiated
    dashboard = Dashboard(id="dashboard")
    forge_builder = ForgeBuilder(id="forge")
    investigator = InvestigatorScreen(id="investigator")
    
    print("[SUCCESS] All screens can be instantiated")
    
    # Test that screens inherit from Screen
    from textual.screen import Screen
    assert isinstance(dashboard, Screen), "Dashboard should inherit from Screen"
    assert isinstance(forge_builder, Screen), "ForgeBuilder should inherit from Screen"
    assert isinstance(investigator, Screen), "InvestigatorScreen should inherit from Screen"
    
    print("[SUCCESS] All screens inherit from Screen")
    
    # Test that app has the correct title
    assert app.TITLE == "DECKFORGE // SRE COCKPIT", f"Title should be 'DECKFORGE // SRE COCKPIT', got '{app.TITLE}'"
    
    print("[SUCCESS] App has correct title")
    
    print("\n[SUCCESS] All structural tests passed!")
    print("The TUI application should now display properly with all components.")

if __name__ == "__main__":
    test_app_structure()