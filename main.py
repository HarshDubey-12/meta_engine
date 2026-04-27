"""Pipeline controller for the meta engine."""

from src.decision.parser import parse_raw_problem
from src.decision.mapper import map_features_to_level
from src.decision.model_selector import select_model_for_level
from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.problem import RawProblem
from src.execution.dispatcher import dispatch_model
from src.execution.runner import run_model


def build_raw_problem(case_name: str) -> RawProblem:
    if case_name == "data":
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
            metadata={"source": "main_data_case"},
        )

    if case_name == "text":
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
            metadata={"source": "main_text_case"},
        )

    if case_name == "equation":
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
            metadata={"source": "main_equation_case"},
        )

    raise ValueError(f"Unsupported case_name: {case_name}")


def build_features() -> ProblemFeatures:
    return ProblemFeatures(
        known_variables=["x", "y", "vx", "vy", "gravity"],
        unknown_variables=["trajectory"],
        dependency_type=DependencyType.TIME,
        mathematical_nature=MathematicalNature.LINEAR,
        variable_count=4,
        representation_type=RepresentationType.EQUATION,
    )


def run_pipeline(raw_problem: RawProblem) -> dict[str, object]:
    structured_problem = parse_raw_problem(raw_problem)
    features = build_features()

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


def main() -> None:
    for case_name in ["data", "text", "equation"]:
        raw_problem = build_raw_problem(case_name)
        summary = run_pipeline(raw_problem)

        result = summary["result"]

        print(f"\n=== Case: {case_name} ===")
        print("Mapped Level:", summary["level"])
        print("Selected Model:", summary["model_type"])
        print("Number of trajectory points:", len(result))
        print("First point:", result[0])
        print("Last point:", result[-1])


if __name__ == "__main__":
    main()
