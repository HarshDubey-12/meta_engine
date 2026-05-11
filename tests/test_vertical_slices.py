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
    """Build named cross-domain executable problem slices."""
    match case_name:
        case "projectile_data":
            return (
                RawProblem(
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
                    metadata={"source": "test_projectile_data"},
                ),
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case "projectile_text":
            return (
                RawProblem(
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
                    metadata={"source": "test_projectile_text"},
                ),
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case "projectile_equation":
            return (
                RawProblem(
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
                    metadata={"source": "test_projectile_equation"},
                ),
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case "projectile_drag_simulation":
            return (
                RawProblem(
                    raw_content={
                        "problem_type": "projectile_problem_with_drag",
                        "output_type": "trajectory",
                        "domain": "mechanics",
                        "initial_state": {
                            "x": 0.0,
                            "y": 0.0,
                            "vx": 10.0,
                            "vy": 20.0,
                        },
                        "parameters": {
                            "gravity": 9.8,
                            "drag_coefficient": 0.015,
                            "duration": 5.0,
                            "dt": 0.05,
                        },
                        "constraints": ["include air resistance"],
                        "simulation_config": {"stop_at_ground": True},
                    },
                    input_type="data",
                    domain="mechanics",
                    constraints=["include air resistance"],
                    metadata={"source": "test_projectile_drag"},
                ),
                ComplexityLevel.LEVEL_3,
                ModelType.SIMULATION,
            )

        case "rc_circuit_ode":
            return (
                RawProblem(
                    raw_content={
                        "problem_type": "rc_circuit_problem",
                        "output_type": "voltage_curve",
                        "domain": "electrical",
                        "initial_state": {"voltage": 5.0},
                        "parameters": {
                            "resistance": 1000.0,
                            "capacitance": 0.001,
                            "duration": 2.0,
                            "dt": 0.1,
                        },
                        "equations": ["dV/dt = -(V / (R * C))"],
                    },
                    input_type="data",
                    domain="electrical",
                    metadata={"source": "test_rc_circuit"},
                ),
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case "cooling_ode":
            return (
                RawProblem(
                    raw_content={
                        "problem_type": "cooling_problem",
                        "output_type": "temperature_curve",
                        "domain": "thermal",
                        "initial_state": {"temperature": 90.0},
                        "parameters": {
                            "ambient_temp": 25.0,
                            "cooling_rate": 0.15,
                            "duration": 5.0,
                            "dt": 0.25,
                        },
                        "equations": ["dT/dt = -k * (T - T_ambient)"],
                    },
                    input_type="data",
                    domain="thermal",
                    metadata={"source": "test_cooling"},
                ),
                ComplexityLevel.LEVEL_2,
                ModelType.ODE,
            )

        case _:
            raise ValueError(f"Unsupported vertical slice case: {case_name}")


@pytest.mark.parametrize(
    "case_name",
    [
        "projectile_data",
        "projectile_text",
        "projectile_equation",
        "projectile_drag_simulation",
        "rc_circuit_ode",
        "cooling_ode",
    ],
)
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

    if case_name.startswith("projectile"):
        assert result[-1]["x"] >= result[0].get("x", 0.0)

    if case_name == "projectile_drag_simulation":
        assert result[-1]["vy"] < result[0]["vy"]

    if case_name == "rc_circuit_ode":
        assert result[-1]["voltage"] < result[0]["voltage"]

    if case_name == "cooling_ode":
        assert result[-1]["temperature"] < result[0]["temperature"]
