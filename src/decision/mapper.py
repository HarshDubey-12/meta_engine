"""Map extracted features to problem levels."""
# Future changes:
# - Replace simple if/else heuristics with configurable rules or a strategy object as complexity grows.
# - Use richer analyzer features, such as equation_count or requires_iteration, to reduce weak guesses.
# - Keep this file responsible only for feature-to-level mapping, not model selection or execution.

from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.level import ComplexityLevel


def map_features_to_level(features: ProblemFeatures) -> ComplexityLevel:
    """Map extracted problem features to a complexity level."""

    if features is None:
        return ComplexityLevel.UNKNOWN

    dynamic_dependencies = {
        DependencyType.TIME,
        DependencyType.SPACE,
        DependencyType.TIME_AND_SPACE,
    }

    # Rule 1: nonlinear dynamic systems require simulation-style handling
    if (
        features.dependency_type in dynamic_dependencies
        and features.mathematical_nature == MathematicalNature.NONLINEAR
    ):
        return ComplexityLevel.LEVEL_3

    # Rule 2: dynamic but not nonlinear systems fit the ODE/calculus path
    if features.dependency_type in dynamic_dependencies:
        return ComplexityLevel.LEVEL_2

    # Rule 3: multi-variable analytical problems
    if (
        features.representation_type == RepresentationType.EQUATION
        and features.variable_count > 3
    ):
        return ComplexityLevel.LEVEL_1

    # Rule 4: direct formula problems
    if features.representation_type in (
        RepresentationType.TEXT,
        RepresentationType.EQUATION,
        RepresentationType.DATA,
    ):
        return ComplexityLevel.LEVEL_0

    return ComplexityLevel.UNKNOWN
