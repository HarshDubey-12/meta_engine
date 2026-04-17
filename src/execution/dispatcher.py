"""Dispatch model identifiers to implementations."""
# Future changes:
# - Replace string placeholders with actual model classes or callable objects.
# - Use a registry dictionary instead of if/else once model implementations stabilize.
# - Add a dedicated SymbolicModel if Level 1 problems need separate behavior.
# - Keep dispatcher focused on lookup only; execution belongs in runner.py.

from src.decision.model_selector import ModelType


def dispatch_model(model_type: ModelType) -> str:
    """Return a placeholder model implementation for the selected model type."""

    # Safety check
    if model_type is None:
        return "UnknownModel"

    if model_type == ModelType.UNKNOWN:
        return "UnknownModel"

    if model_type == ModelType.ANALYTICAL:
        return "AnalyticalModel"

    if model_type == ModelType.SYMBOLIC:
        return "AnalyticalModel"

    if model_type == ModelType.ODE:
        return "ODEModel"

    if model_type == ModelType.SIMULATION:
        return "SimulationModel"

    # Fallback
    return "UnknownModel"