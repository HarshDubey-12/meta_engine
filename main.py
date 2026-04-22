"""Pipeline controller for the meta engine."""

from src.decision.mapper import map_features_to_level
from src.decision.model_selector import select_model_for_level
from src.definitions.features import (
    DependencyType,
    MathematicalNature,
    ProblemFeatures,
    RepresentationType,
)
from src.definitions.problem import RawProblem, StructuredProblem
from src.execution.dispatcher import dispatch_model
from src.execution.runner import run_model


def main() -> None:
    raw_problem = RawProblem(
        raw_content="Projectile motion without air resistance",
        input_type="text",
        domain="mechanics",
        constraints=["ignore air resistance"],
        metadata={"source": "manual_test"},
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

    level = map_features_to_level(features)
    model_type = select_model_for_level(level)
    model_function = dispatch_model(model_type)
    result = run_model(structured_problem, model_function)

    print("Mapped Level:", level)
    print("Selected Model:", model_type)
    print("Number of trajectory points:", len(result))
    print("First point:", result[0])
    print("Last point:", result[-1])


if __name__ == "__main__":
    main()
