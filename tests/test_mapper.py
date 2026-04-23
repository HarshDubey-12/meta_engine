from src.decision.mapper import map_features_to_level
from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.level import ComplexityLevel


def test_mapper_returns_level_2_for_time_dependent_equation_problem() -> None:
    features = ProblemFeatures(
        known_variables=["x", "y", "vx", "vy"],
        unknown_variables=["trajectory"],
        dependency_type=DependencyType.TIME,
        mathematical_nature=MathematicalNature.LINEAR,
        variable_count=4,
        representation_type=RepresentationType.EQUATION,
    )

    level = map_features_to_level(features)

    assert level == ComplexityLevel.LEVEL_2
