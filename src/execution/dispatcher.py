"""Dispatch model identifiers to implementations."""
# Future changes:
# - Replace unsupported branches with actual model classes or callable objects.
# - Use a registry dictionary instead of if/else once model implementations stabilize.
# - Add a dedicated SymbolicModel if Level 1 problems need separate behavior.
# - Keep dispatcher focused on lookup only; execution belongs in runner.py.

from collections.abc import Callable

from src.decision.model_selector import ModelType
from src.definitions.problem import StructuredProblem
from src.models.ode import solve_ode_problem


def dispatch_model(
    model_type: ModelType,
) -> Callable[[StructuredProblem], list[dict[str, float]]]:
    """Return the executable model implementation for the selected model type."""

    if model_type is None:
        raise ValueError("model_type is required.")

    if model_type == ModelType.ODE:
        return solve_ode_problem

    raise ValueError(f"Unsupported model type: {model_type}")
