"""ODE model implementations."""
from src.computations.ode_methods.euler import euler_integrate
from src.definitions.problem import StructuredProblem


def solve_ode_problem(problem: StructuredProblem) -> list[dict[str, float]]:
    """Solve supported ODE problems using a numerical integration method."""
    if problem is None:
        raise ValueError("problem is required.")
    if not problem.problem_type:
        raise ValueError("problem_type is required.")
    if not problem.initial_state:
        raise ValueError("initial_state is required.")

    initial_state = problem.initial_state
    parameters = problem.parameters

    start_time = 0.0
    end_time = parameters.get("duration")
    dt = parameters.get("dt")
    gravity = parameters.get("gravity")

    if end_time is None:
        raise ValueError("duration parameter is required.")
    if dt is None:
        raise ValueError("dt parameter is required.")
    derivative_function = _build_derivative_function(problem)

    return euler_integrate(
        derivative_function,
        initial_state,
        start_time,
        end_time,
        dt,
    )


def _build_derivative_function(problem: StructuredProblem):
    parameters = problem.parameters

    if problem.problem_type == "projectile_problem":
        gravity = parameters.get("gravity")

        if gravity is None:
            raise ValueError("gravity parameter is required.")

        def projectile_derivatives(
            current_time: float,
            current_state: dict[str, float],
        ) -> dict[str, float]:
            """Return derivatives for projectile motion without air resistance."""
            _ = current_time
            return {
                "x": current_state["vx"],
                "y": current_state["vy"],
                "vx": 0.0,
                "vy": -float(gravity),
            }

        return projectile_derivatives

    if problem.problem_type == "rc_circuit_problem":
        resistance = parameters.get("resistance")
        capacitance = parameters.get("capacitance")

        if resistance is None:
            raise ValueError("resistance parameter is required.")
        if capacitance is None:
            raise ValueError("capacitance parameter is required.")

        def rc_circuit_derivatives(
            current_time: float,
            current_state: dict[str, float],
        ) -> dict[str, float]:
            """Return the first-order RC discharge derivative."""
            _ = current_time
            voltage = current_state["voltage"]
            return {
                "voltage": -(voltage / (float(resistance) * float(capacitance))),
            }

        return rc_circuit_derivatives

    if problem.problem_type == "cooling_problem":
        ambient_temp = parameters.get("ambient_temp")
        cooling_rate = parameters.get("cooling_rate")

        if ambient_temp is None:
            raise ValueError("ambient_temp parameter is required.")
        if cooling_rate is None:
            raise ValueError("cooling_rate parameter is required.")

        def cooling_derivatives(
            current_time: float,
            current_state: dict[str, float],
        ) -> dict[str, float]:
            """Return Newton cooling derivatives."""
            _ = current_time
            temperature = current_state["temperature"]
            return {
                "temperature": -float(cooling_rate) * (temperature - float(ambient_temp)),
            }

        return cooling_derivatives

    raise ValueError(f"Unsupported ODE problem_type: {problem.problem_type}")
