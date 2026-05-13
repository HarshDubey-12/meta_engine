"""Pipeline controller for the meta engine."""

from src.decision.analyzer import analyze_problem
from src.decision.mapper import map_features_to_level
from src.decision.model_selector import select_model_for_level
from src.decision.parser import parse_raw_problem
from src.definitions.problem import RawProblem
from src.execution.dispatcher import dispatch_model
from src.execution.runner import run_model


def build_raw_problem(case_name: str) -> RawProblem:
    if case_name == "projectile_data":
        return RawProblem(
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
            metadata={"source": "main_projectile_data_case"},
        )

    if case_name == "projectile_text":
        return RawProblem(
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
            metadata={"source": "main_projectile_text_case"},
        )

    if case_name == "projectile_equation":
        return RawProblem(
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
            metadata={"source": "main_projectile_equation_case"},
        )

    if case_name == "projectile_drag_simulation":
        return RawProblem(
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
            metadata={"source": "main_projectile_drag_case"},
        )

    if case_name == "rc_circuit_ode":
        return RawProblem(
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
            metadata={"source": "main_rc_case"},
        )

    if case_name == "cooling_ode":
        return RawProblem(
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
            metadata={"source": "main_cooling_case"},
        )

    raise ValueError(f"Unsupported case_name: {case_name}")


def run_pipeline(raw_problem: RawProblem) -> dict[str, object]:
    structured_problem = parse_raw_problem(raw_problem)
    features = analyze_problem(structured_problem)
    level = map_features_to_level(features)
    model_type = select_model_for_level(level)
    model_function = dispatch_model(model_type)
    result = run_model(structured_problem, model_function)

    return {
        "raw_problem": raw_problem,
        "structured_problem": structured_problem,
        "features": features,
        "level": level,
        "model_type": model_type,
        "result": result,
    }


def _print_result_summary(case_name: str, summary: dict[str, object]) -> None:
    result = summary["result"]

    print(f"\n=== Case: {case_name} ===")
    print("Problem Type:", summary["structured_problem"].problem_type)
    print("Mapped Level:", summary["level"])
    print("Selected Model:", summary["model_type"])
    print("Representation Type:", summary["features"].representation_type)

    if isinstance(result, list):
        print("Number of states:", len(result))
        print("First state:", result[0])
        print("Last state:", result[-1])
        return

    if isinstance(result, dict):
        print("Result Keys:", list(result.keys()))
        return

    print("Result:", result)


def main() -> None:
    cases = [
        "projectile_data",
        "projectile_text",
        "projectile_equation",
        "projectile_drag_simulation",
        "rc_circuit_ode",
        "cooling_ode",
    ]

    for case_name in cases:
        raw_problem = build_raw_problem(case_name)
        summary = run_pipeline(raw_problem)
        _print_result_summary(case_name, summary)


if __name__ == "__main__":
    main()
