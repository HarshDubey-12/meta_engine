import pytest

from src.decision.analyzer import analyze_problem
from src.decision.mapper import map_features_to_level
from src.decision.model_selector import ModelType, select_model_for_level
from src.decision.parser import parse_raw_problem
from src.definitions.level import ComplexityLevel
from src.definitions.problem import RawProblem
from src.execution.dispatcher import dispatch_model
from src.execution.runner import run_model


def build_vertical_slice_case(
    case_name: str,
) -> tuple[RawProblem, ComplexityLevel, ModelType]:
    """Build a named vertical-slice test case.

    Extend this match/case block as new executable problem slices are added.
    """
    match case_name:
        case "data":
            raw_problem = RawProblem(
                raw_content={
                    "problem_type": "projectile_problem",
                    "output_type": "trajectory",
                    "initial_state": {
                        "x": 0.0,
                        "y": 0.0,
                        "vx": 10.0,
                        "vy": 20.0,
                    },
                    "parameters": {
                        "gravity": 9.8,
                        "duration": 5.0,
                        "dt": 0.1,
                    },
                    "equations": [
                        "dx/dt = vx",
                        "dy/dt = vy",
                        "dvx/dt = 0",
                        "dvy/dt = -gravity",
                    ],
                    "constraints": ["ignore air resistance"],
                },
                input_type="data",
                domain="mechanics",
                constraints=["ignore air resistance"],
                metadata={"source": "test_data_case"},
            )

            return raw_problem, ComplexityLevel.LEVEL_2, ModelType.ODE

        case "text":
            raw_problem = RawProblem(
                raw_content=(
                    "problem_type: projectile_problem\n"
                    "output_type: trajectory\n"
                    "domain: mechanics\n"
                    "x: 0\n"
                    "y: 0\n"
                    "vx: 10\n"
                    "vy: 20\n"
                    "gravity: 9.8\n"
                    "duration: 5\n"
                    "dt: 0.1\n"
                    "constraint: ignore air resistance\n"
                ),
                input_type="text",
                domain="mechanics",
                constraints=["ignore air resistance"],
                metadata={"source": "test_text_case"},
            )

            return raw_problem, ComplexityLevel.LEVEL_2, ModelType.ODE

        case "equation":
            raw_problem = RawProblem(
                raw_content=(
                    "problem_type: projectile_problem\n"
                    "output_type: trajectory\n"
                    "domain: mechanics\n"
                    "x: 0\n"
                    "y: 0\n"
                    "vx: 10\n"
                    "vy: 20\n"
                    "gravity: 9.8\n"
                    "duration: 5\n"
                    "dt: 0.1\n"
                    "equation: dx/dt = vx\n"
                    "equation: dy/dt = vy\n"
                    "equation: dvx/dt = 0\n"
                    "equation: dvy/dt = -gravity\n"
                    "constraint: ignore air resistance\n"
                ),
                input_type="equation",
                domain="mechanics",
                constraints=["ignore air resistance"],
                metadata={"source": "test_equation_case"},
            )

            return raw_problem, ComplexityLevel.LEVEL_2, ModelType.ODE

        case _:
            raise ValueError(f"Unsupported vertical slice case: {case_name}")


@pytest.mark.parametrize("case_name", ["data", "text", "equation"])
def test_vertical_slice_pipeline(case_name: str) -> None:
    raw_problem, expected_level, expected_model_type = build_vertical_slice_case(
        case_name
    )

    structured_problem = parse_raw_problem(raw_problem)
    features = analyze_problem(structured_problem)
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
