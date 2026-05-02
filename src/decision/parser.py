"""Parse raw inputs into structured chunks."""
# Future changes:
# - Expand text parsing from constrained key-value input to richer natural-language normalization.
# - Replace branch-specific hardcoded field routing with reusable parsing utilities or parser strategies.
# - Add richer equation parsing so symbolic structure can be preserved beyond plain equation strings.
# - Support image/document input through OCR or document extraction before normalization.
# - Keep parser focused on structure extraction only; feature inference belongs in analyzer.py.

from src.definitions.problem import RawProblem, StructuredProblem


def _parse_data_problem(raw_problem: RawProblem) -> StructuredProblem:
    """Parse structured data input into a StructuredProblem."""
    content = raw_problem.raw_content

    if not isinstance(content, dict):
        raise ValueError("Data input requires raw_content to be a dictionary.")

    problem_type = content.get("problem_type")
    output_type = content.get("output_type")
    domain = content.get("domain", raw_problem.domain)
    initial_state = content.get("initial_state", {})
    parameters = content.get("parameters", {})
    equations = content.get("equations", [])
    constraints = content.get("constraints", raw_problem.constraints)
    simulation_config = content.get("simulation_config", {})

    if not problem_type:
        raise ValueError("problem_type is required in data input.")
    if not output_type:
        raise ValueError("output_type is required in data input.")
    if not isinstance(initial_state, dict):
        raise ValueError("initial_state must be a dictionary.")
    if not isinstance(parameters, dict):
        raise ValueError("parameters must be a dictionary.")
    if not isinstance(equations, list):
        raise ValueError("equations must be a list.")
    if not isinstance(constraints, list):
        raise ValueError("constraints must be a list.")
    if not isinstance(simulation_config, dict):
        raise ValueError("simulation_config must be a dictionary.")

    return StructuredProblem(
        problem_type=problem_type,
        output_type=output_type,
        domain=domain,
        source_problem=raw_problem,
        initial_state=initial_state,
        parameters=parameters,
        equations=equations,
        constraints=constraints,
        simulation_config=simulation_config,
    )


def _parse_text_problem(raw_problem: RawProblem) -> StructuredProblem:
    """Parse constrained key-value text input into a StructuredProblem."""
    content = raw_problem.raw_content

    if content is None:
        raise ValueError("raw_content should not be empty.")
    if not isinstance(content, str):
        raise ValueError("Text input requires raw_content to be a string.")

    lines = content.strip().splitlines()
    clean_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            clean_lines.append(stripped_line)

    problem_type = None
    output_type = None
    domain = raw_problem.domain
    initial_state = {}
    parameters = {}
    constraints = []

    for line in clean_lines:
        if ":" not in line:
            raise ValueError("Each line must contain ':'.")

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "problem_type":
            problem_type = value
        elif key == "output_type":
            output_type = value
        elif key == "domain":
            domain = value
        elif key in ["x", "y", "vx", "vy"]:
            initial_state[key] = float(value)
        elif key in ["gravity", "duration", "dt"]:
            parameters[key] = float(value)
        elif key == "constraint":
            constraints.append(value)
        else:
            raise ValueError(f"Unsupported text field: {key}")

    if not problem_type:
        raise ValueError("problem_type is required in text input.")
    if not output_type:
        raise ValueError("output_type is required in text input.")

    return StructuredProblem(
        problem_type=problem_type,
        output_type=output_type,
        domain=domain,
        source_problem=raw_problem,
        initial_state=initial_state,
        parameters=parameters,
        constraints=constraints,
    )


def _parse_equation_problem(raw_problem: RawProblem) -> StructuredProblem:
    """Parse constrained equation input into a StructuredProblem."""
    content = raw_problem.raw_content

    if content is None:
        raise ValueError("raw_content should not be empty.")
    if not isinstance(content, str):
        raise ValueError("Equation input requires raw_content to be a string.")

    lines = content.strip().splitlines()
    clean_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            clean_lines.append(stripped_line)

    problem_type = None
    output_type = None
    domain = raw_problem.domain
    initial_state = {}
    parameters = {}
    equations = []
    constraints = []

    for line in clean_lines:
        if ":" not in line:
            raise ValueError("Each line must contain ':'.")

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "problem_type":
            problem_type = value
        elif key == "output_type":
            output_type = value
        elif key == "domain":
            domain = value
        elif key in ["x", "y", "vx", "vy"]:
            initial_state[key] = float(value)
        elif key in ["gravity", "duration", "dt"]:
            parameters[key] = float(value)
        elif key == "equation":
            equations.append(value)
        elif key == "constraint":
            constraints.append(value)
        else:
            raise ValueError(f"Unsupported equation field: {key}")

    if not problem_type:
        raise ValueError("problem_type is required in equation input.")
    if not output_type:
        raise ValueError("output_type is required in equation input.")

    return StructuredProblem(
        problem_type=problem_type,
        output_type=output_type,
        domain=domain,
        source_problem=raw_problem,
        initial_state=initial_state,
        parameters=parameters,
        equations=equations,
        constraints=constraints,
    )


def parse_raw_problem(raw_problem: RawProblem) -> StructuredProblem:
    """Route a RawProblem to the appropriate parsing branch."""
    if raw_problem is None:
        raise ValueError("raw_problem is required.")
    if not raw_problem.input_type:
        raise ValueError("input_type is required.")
    if raw_problem.raw_content is None:
        raise ValueError("raw_content is required.")

    if raw_problem.input_type == "data":
        return _parse_data_problem(raw_problem)
    if raw_problem.input_type == "text":
        return _parse_text_problem(raw_problem)
    if raw_problem.input_type == "equation":
        return _parse_equation_problem(raw_problem)

    raise ValueError(f"Unsupported input_type: {raw_problem.input_type}")
