import json
from core.schema import InfraBlueprint, ComputeResource

class ProviderFactory:
    """Maps generic intents to cloud-specific SKUs using lookup table."""

    def __init__(self):
        # In production, load from DB or a JSON config file
        self.mappings = {
            "aws": {"small": "t3.medium", "large": "m5.large"},
            "azure": {"small": "Standard_B2s", "large": "Standard_D2_v3"},
            "gcp": {"small": "e2-medium", "large": "e2-standard-2"}
        }

    def get_sku(self, provider: str, intent: ComputeResource) -> str:
        size = "small" if intent.cpu <= 2 else "large"
        return self.mappings.get(provider.lower(), {}).get(size, "default_sku")

    def compile_to_provider_specific(self, blueprint: InfraBlueprint, provider: str):
        """Convert generic blueprint to provider-specific configuration."""
        # This would typically involve more complex transformations
        # For now, we'll map the generic specs to provider-specific SKUs
        sku_mapping = {}

        # Example transformation logic
        if hasattr(blueprint, 'app_config') and blueprint.app_config.enabled:
            # Create a default ComputeResource for the app server
            compute_intent = ComputeResource(cpu=2, memory="4GB", disk="50GB", resource_type="app_server")
            sku = self.get_sku(provider, compute_intent)
            sku_mapping['app_server'] = sku

        return {
            "provider": provider,
            "region": blueprint.region,
            "resources": sku_mapping,
            "configuration": blueprint.model_dump()
        }