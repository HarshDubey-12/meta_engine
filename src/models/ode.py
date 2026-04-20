"""ODE model implementations."""
from src.computations.ode_methods.euler import euler_integrate
from src.definitions.problem import StructuredProblem


def solve_ode_problem(problem: StructuredProblem) -> list[dict[str, float]]:
    """Solve supported ODE problems using a numerical integration method."""
    if problem.problem_type != "projectile_problem":
        raise ValueError("problem_type should be projectile_problem.")

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
    if gravity is None:
        raise ValueError("gravity parameter is required.")

    def projectile_derivatives(
        current_time: float,
        current_state: dict[str, float],
    ) -> dict[str, float]:
        """Return derivatives for projectile motion without air resistance."""
        return {
            "x": current_state["vx"],
            "y": current_state["vy"],
            "vx": 0.0,
            "vy": -gravity,
        }

    return euler_integrate(
        projectile_derivatives,
        initial_state,
        start_time,
        end_time,
        dt,
    )
