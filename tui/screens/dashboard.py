from textual.screen import Screen
from textual.widgets import Sparkline, DataTable, Label, Static
from textual.containers import Grid, Vertical
from textual.reactive import reactive
from textual.app import ComposeResult

class Dashboard(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("[bold]SYSTEM TELEMETRY[/bold]"),
            Grid(
                Vertical(Label("CPU %"), Sparkline([], id="cpu-spark"), classes="stat-card"),
                Vertical(Label("MEM GB"), Sparkline([], id="mem-spark"), classes="stat-card"),
                id="metrics-grid"
            ),
            DataTable(id="agent-table"),
            Static(id="cost-display", classes="stat-card")
        )

    def on_mount(self) -> None:
        table = self.query_one("#agent-table", DataTable)
        table.add_columns("ID", "Agent", "Status", "Runtime")
        
        # Set up a periodic callback to update metrics
        self.set_interval(2.0, self.update_metrics)
    
    def update_metrics(self) -> None:
        """Update metrics from the parent app."""
        app = self.app
        if hasattr(app, 'metrics') and app.metrics:
            metrics = app.metrics
            self.query_one("#cpu-spark").data = metrics.cpu_history
            self.query_one("#mem-spark").data = metrics.mem_history
            self.query_one("#cost-display").update(f"Monthly Burn: ${metrics.total_cost:,.2f}")

            table = self.query_one("#agent-table")
            table.clear()
            for task in metrics.active_tasks:
                table.add_row(task.id, task.agent, task.status, task.runtime)