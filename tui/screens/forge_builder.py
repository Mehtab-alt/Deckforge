from textual import on, work
from textual.screen import Screen
from textual.widgets import Tree, TextArea, Static, Label
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.app import ComposeResult

class ForgeBuilder(Screen):
    BINDINGS = [
        Binding("f5", "deploy_diff", "Deploy"),
        Binding("ctrl+a", "open_snippet_library", "Inject Snippet")
    ]

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("TOPOLOGY")
                yield Tree("Templates", id="topology-tree")
            with Vertical():
                yield TextArea(language="yaml", id="editor")
                yield Static("Status: Ready", id="validator-bar")

    async def on_mount(self) -> None:
        # For demo purposes, populate with sample structure
        structure = {
            "terraform": ["main.tf", "variables.tf", "outputs.tf"],
            "ansible": ["playbook.yml", "inventory.ini"],
            "docker": ["Dockerfile", "docker-compose.yml"]
        }
        self._populate_tree(self.query_one("#topology-tree").root, structure)

    def _populate_tree(self, parent, structure):
        """Helper to populate the tree with structure data."""
        for key, value in structure.items():
            if isinstance(value, list):
                node = parent.add_leaf(key)
                for item in value:
                    node.add_leaf(item)
            else:
                node = parent.add_leaf(f"{key}: {value}")

    @on(TextArea.Changed)
    def debounced_validation(self) -> None:
        self.set_timer(0.5, self.perform_validation)

    async def perform_validation(self) -> None:
        content = self.query_one("#editor").text
        # For demo purposes, we'll simulate validation
        bar = self.query_one("#validator-bar")
        if len(content) > 10:
            bar.update("[green]✓ Valid[/]")
            bar.styles.background = "#004400"
        else:
            bar.update(f"[red]✗ Not enough content[/]")
            bar.styles.background = "#440000"

    def action_open_snippet_library(self) -> None:
        """SRE alternative to drag-and-drop: Keyboard-driven injection."""
        # Implementation of snippet selection modal that inserts text at cursor
        pass
        
    def action_deploy_diff(self) -> None:
        """Deploy the current changes."""
        # Implementation for deploying changes
        pass