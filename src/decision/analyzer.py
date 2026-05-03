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
    if not problem.problem_type:
        raise ValueError("problem_type is required.")

    known_variables = list(problem.initial_state.keys()) + list(problem.parameters.keys())
    unknown_variables = [problem.output_type]
    variable_count = len(problem.initial_state)
    representation_type = _infer_representation_type(problem)
    dependency_type = _infer_dependency_type(problem)
    mathematical_nature = _infer_mathematical_nature(problem)

    return ProblemFeatures(
        known_variables=known_variables,
        unknown_variables=unknown_variables,
        dependency_type=dependency_type,
        mathematical_nature=mathematical_nature,
        variable_count=variable_count,
        representation_type=representation_type,
    )


def _infer_representation_type(problem: StructuredProblem) -> RepresentationType:
    source_input_type = None

    if problem.source_problem is not None:
        source_input_type = problem.source_problem.input_type

    if source_input_type == "data":
        return RepresentationType.DATA
    if source_input_type == "text":
        return RepresentationType.TEXT
    if source_input_type == "equation":
        return RepresentationType.EQUATION

    return RepresentationType.UNKNOWN


def _infer_dependency_type(problem: StructuredProblem) -> DependencyType:
    normalized_equations = [equation.lower() for equation in problem.equations]

    has_time_dependency = (
        "duration" in problem.parameters
        or "dt" in problem.parameters
        or any("/dt" in equation for equation in normalized_equations)
    )
    has_space_dependency = any("/dx" in equation for equation in normalized_equations)

    if has_time_dependency and has_space_dependency:
        return DependencyType.TIME_AND_SPACE
    if has_time_dependency:
        return DependencyType.TIME
    if has_space_dependency:
        return DependencyType.SPACE

    if problem.problem_type in {
        "projectile_problem",
        "projectile_problem_with_drag",
        "rc_circuit_problem",
        "cooling_problem",
    }:
        return DependencyType.TIME

    return DependencyType.UNKNOWN


def _infer_mathematical_nature(problem: StructuredProblem) -> MathematicalNature:
    normalized_problem_type = problem.problem_type.lower()
    normalized_constraints = [constraint.lower() for constraint in problem.constraints]
    normalized_equations = [equation.lower() for equation in problem.equations]

    if "drag" in normalized_problem_type:
        return MathematicalNature.NONLINEAR

    if any("nonlinear" in constraint for constraint in normalized_constraints):
        return MathematicalNature.NONLINEAR

    nonlinear_tokens = ("^", "**", "sin(", "cos(", "exp(", "log(")
    if any(token in equation for equation in normalized_equations for token in nonlinear_tokens):
        return MathematicalNature.NONLINEAR

    if problem.problem_type in {
        "projectile_problem",
        "rc_circuit_problem",
        "cooling_problem",
    }:
        return MathematicalNature.LINEAR

    return MathematicalNature.UNKNOWN
