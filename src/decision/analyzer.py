"""Extract features from structured inputs."""

from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.problem import StructuredProblem


def analyze_problem(problem: StructuredProblem) -> ProblemFeatures:
    if problem is None:
        raise ValueError("problem is required.")

    if problem.problem_type != "projectile_problem":
        raise ValueError(f"Unsupported problem_type: {problem.problem_type}")

    known_variables = list(problem.initial_state.keys()) + list(problem.parameters.keys())
    unknown_variables = [problem.output_type]

    source_input_type = None
    if problem.source_problem is not None:
        source_input_type = problem.source_problem.input_type

    if source_input_type == "data":
        representation_type = RepresentationType.DATA
    elif source_input_type == "text":
        representation_type = RepresentationType.TEXT
    elif source_input_type == "equation":
        representation_type = RepresentationType.EQUATION
    else:
        representation_type = RepresentationType.UNKNOWN

    variable_count = len(problem.initial_state)

    dependency_type = DependencyType.TIME
    mathematical_nature = MathematicalNature.LINEAR

    return ProblemFeatures(
        known_variables=known_variables,
        unknown_variables=unknown_variables,
        dependency_type=dependency_type,
        mathematical_nature=mathematical_nature,
        variable_count=variable_count,
        representation_type=representation_type,
    )
