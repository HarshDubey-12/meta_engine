"""Execution runner for selected models."""
from collections.abc import Callable

from src.definitions.problem import StructuredProblem

def run_model(
        problem: StructuredProblem,
        model_function: Callable[[StructuredProblem],object]
        )->object:
    if model_function is None:
        raise ValueError("model_function is required.")
    if problem is None:
        raise ValueError("problem is required.")
    
    return model_function(problem)