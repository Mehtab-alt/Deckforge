import os
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, ContentSwitcher, Static
from textual.binding import Binding
from tui.bridge import APIBridge
from tui.screens.dashboard import Dashboard
from tui.screens.forge_builder import ForgeBuilder
from tui.screens.investigator import InvestigatorScreen

class DeckForgeApp(App):
    # CSS_PATH = "style.tcss"  # Temporarily disabled due to CSS parsing issues with Textual's internal styles
    TITLE = "DECKFORGE // SRE COCKPIT"
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Exit"),
        Binding("ctrl+d", "switch_tab('dashboard')", "Dashboard"),
        Binding("ctrl+f", "switch_tab('forge')", "Forge Engine"),
        Binding("ctrl+i", "switch_tab('investigator')", "SRE Investigator"),
        Binding("ctrl+p", "command_palette", "Search"),
    ]

    # Reactive Global State
    metrics = reactive(None)
    connection_status = reactive("CONNECTING")

    def __init__(self):
        super().__init__()
        self.api = APIBridge(os.getenv("API_URL", "http://localhost:8000"), os.getenv("API_KEY", "dummy-key"))

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ContentSwitcher(
            Dashboard(id="dashboard"),
            ForgeBuilder(id="forge"),
            InvestigatorScreen(id="investigator"),
            initial="dashboard"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(2.0, self.refresh_global_metrics)

    async def refresh_global_metrics(self):
        try:
            # For demo purposes, we'll simulate metrics
            from core.schema import SystemMetrics, AgentTask
            self.metrics = SystemMetrics(
                cpu_history=[50, 55, 60, 65, 70, 75, 80, 85],
                mem_history=[2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5],
                total_cost=12345.67,
                active_tasks=[
                    AgentTask(id="task-1", agent="orchestrator", status="RUNNING", runtime="00:15:32"),
                    AgentTask(id="task-2", agent="investigator", status="IDLE", runtime="00:05:12")
                ]
            )
            self.connection_status = "ONLINE"
        except:
            self.connection_status = "DEGRADED"

    def action_switch_tab(self, tab: str) -> None:
        self.query_one(ContentSwitcher).current = tab