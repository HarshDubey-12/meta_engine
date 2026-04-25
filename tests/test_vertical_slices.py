import pytest

from src.decision.mapper import map_features_to_level
from src.decision.model_selector import ModelType, select_model_for_level
from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.level import ComplexityLevel
from src.definitions.problem import RawProblem, StructuredProblem
from src.execution.dispatcher import dispatch_model
from src.execution.runner import run_model


def build_vertical_slice_case(
    case_name: str,
) -> tuple[StructuredProblem, ProblemFeatures, ComplexityLevel, ModelType]:
    """Build a named vertical-slice test case.

    Extend this match/case block as new executable problem slices are added.
    """
    match case_name:
        case "projectile_problem":
            raw_problem = RawProblem(
                raw_content="Projectile motion without air resistance",
                input_type="text",
                domain="mechanics",
                constraints=["ignore air resistance"],
                metadata={"source": "test"},
            )

            structured_problem = StructuredProblem(
                problem_type="projectile_problem",
                output_type="trajectory",
                domain="mechanics",
                source_problem=raw_problem,
                initial_state={
                    "x": 0.0,
                    "y": 0.0,
                    "vx": 10.0,
                    "vy": 20.0,
                },
                parameters={
                    "gravity": 9.81,
                    "duration": 5.0,
                    "dt": 0.1,
                },
                constraints=["ignore air resistance"],
            )

            features = ProblemFeatures(
                known_variables=["x", "y", "vx", "vy", "gravity"],
                unknown_variables=["trajectory"],
                dependency_type=DependencyType.TIME,
                mathematical_nature=MathematicalNature.LINEAR,
                variable_count=4,
                representation_type=RepresentationType.EQUATION,
            )

            return (
                structured_problem,
                features,
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case _:
            raise ValueError(f"Unsupported vertical slice case: {case_name}")


@pytest.mark.parametrize("case_name", ["projectile_problem"])
def test_vertical_slice_pipeline(case_name: str) -> None:
    (
        structured_problem,
        features,
        expected_level,
        expected_model_type,
    ) = build_vertical_slice_case(case_name)

    level = map_features_to_level(features)
    model_type = select_model_for_level(level)
    model_function = dispatch_model(model_type)
    result = run_model(structured_problem, model_function)

    assert level == expected_level
    assert model_type == expected_model_type
    assert isinstance(result, list)
    assert len(result) > 1
    assert result[0]["time"] == 0.0
    assert result[0]["x"] == 0.0
    assert result[0]["y"] == 0.0
    assert result[-1]["x"] > result[0]["x"]
    assert result[-1]["vy"] < result[0]["vy"]
