from src.decision.parser import parse_raw_problem
from src.definitions.problem import RawProblem


def test_parse_raw_problem_parses_data_input() -> None:
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
                "gravity": 9.81,
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
    )

    structured_problem = parse_raw_problem(raw_problem)

    assert structured_problem.problem_type == "projectile_problem"
    assert structured_problem.output_type == "trajectory"
    assert structured_problem.domain == "mechanics"
    assert structured_problem.source_problem == raw_problem
    assert structured_problem.initial_state["vx"] == 10.0
    assert structured_problem.parameters["gravity"] == 9.81
    assert structured_problem.equations[0] == "dx/dt = vx"
    assert structured_problem.constraints == ["ignore air resistance"]


def test_parse_raw_problem_parses_text_input() -> None:
    raw_problem = RawProblem(
        raw_content=(
            "problem_type: projectile_problem\n"
            "output_type: trajectory\n"
            "domain: mechanics\n"
            "x: 0\n"
            "y: 0\n"
            "vx: 10\n"
            "vy: 20\n"
            "gravity: 9.81\n"
            "duration: 5\n"
            "dt: 0.1\n"
            "constraint: ignore air resistance\n"
        ),
        input_type="text",
        domain="mechanics",
    )

    structured_problem = parse_raw_problem(raw_problem)

    assert structured_problem.problem_type == "projectile_problem"
    assert structured_problem.output_type == "trajectory"
    assert structured_problem.domain == "mechanics"
    assert structured_problem.source_problem == raw_problem
    assert structured_problem.initial_state["x"] == 0.0
    assert structured_problem.initial_state["vy"] == 20.0
    assert structured_problem.parameters["duration"] == 5.0
    assert structured_problem.constraints == ["ignore air resistance"]


def test_parse_raw_problem_parses_equation_input() -> None:
    raw_problem = RawProblem(
        raw_content=(
            "problem_type: projectile_problem\n"
            "output_type: trajectory\n"
            "domain: mechanics\n"
            "x: 0\n"
            "y: 0\n"
            "vx: 10\n"
            "vy: 20\n"
            "gravity: 9.81\n"
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
    )

    structured_problem = parse_raw_problem(raw_problem)

    assert structured_problem.problem_type == "projectile_problem"
    assert structured_problem.output_type == "trajectory"
    assert structured_problem.domain == "mechanics"
    assert structured_problem.source_problem == raw_problem
    assert structured_problem.initial_state["y"] == 0.0
    assert structured_problem.parameters["dt"] == 0.1
    assert len(structured_problem.equations) == 4
    assert structured_problem.equations[-1] == "dvy/dt = -gravity"
    assert structured_problem.constraints == ["ignore air resistance"]
