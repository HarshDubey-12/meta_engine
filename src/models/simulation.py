"""Simulation model implementations."""
from collections.abc import Callable
from copy import deepcopy
import random

from src.computations.monte_carlo import run_monte_carlo
from src.definitions.problem import StructuredProblem


def solve_simulation_problem(problem: StructuredProblem) -> object:
    """Solve supported dynamic systems using discrete simulation."""

    if problem is None:
        raise ValueError("problem is required.")
    if not problem.problem_type:
        raise ValueError("problem_type is required.")
    if not problem.initial_state:
        raise ValueError("initial_state is required.")

    parameters = problem.parameters
    duration = parameters.get("duration")
    dt = parameters.get("dt")

    if duration is None:
        raise ValueError("duration parameter is required.")
    if dt is None:
        raise ValueError("dt parameter is required.")
    if dt <= 0:
        raise ValueError("dt must be positive.")

    if problem.simulation_config.get("use_monte_carlo", False):
        return _solve_with_monte_carlo(problem)

    step_function = _build_step_function(problem)
    stop_condition = _build_stop_condition(problem)

    return _run_simulation_loop(
        step_function=step_function,
        initial_state=problem.initial_state,
        start_time=0.0,
        end_time=float(duration),
        dt=float(dt),
        stop_condition=stop_condition,
    )


def _run_simulation_loop(
    step_function: Callable[[dict[str, float], float], dict[str, float]],
    initial_state: dict[str, object],
    start_time: float,
    end_time: float,
    dt: float,
    stop_condition: Callable[[dict[str, float], float], bool] | None = None,
) -> list[dict[str, float]]:
    current_time = start_time
    current_state = {key: float(value) for key, value in initial_state.items()}

    trajectory: list[dict[str, float]] = []
    trajectory.append({"time": current_time, **current_state})

    while current_time < end_time:
        next_state = step_function(current_state, dt)
        current_time = current_time + dt

        trajectory.append({"time": current_time, **next_state})
        current_state = next_state

        if stop_condition is not None and stop_condition(current_state, current_time):
            break

    return trajectory


def _build_step_function(
    problem: StructuredProblem,
) -> Callable[[dict[str, float], float], dict[str, float]]:
    parameters = problem.parameters

    if problem.problem_type == "projectile_problem_with_drag":
        gravity = float(parameters["gravity"])
        drag_coefficient = float(parameters["drag_coefficient"])

        def step(current_state: dict[str, float], dt: float) -> dict[str, float]:
            x = current_state["x"]
            y = current_state["y"]
            vx = current_state["vx"]
            vy = current_state["vy"]
            speed = (vx**2 + vy**2) ** 0.5

            ax = -(drag_coefficient * speed * vx)
            ay = -gravity - (drag_coefficient * speed * vy)

            next_vx = vx + (ax * dt)
            next_vy = vy + (ay * dt)
            next_x = x + (next_vx * dt)
            next_y = y + (next_vy * dt)

            return {
                "x": next_x,
                "y": next_y,
                "vx": next_vx,
                "vy": next_vy,
            }

        return step

    if problem.problem_type == "rc_circuit_problem":
        resistance = float(parameters["resistance"])
        capacitance = float(parameters["capacitance"])

        def step(current_state: dict[str, float], dt: float) -> dict[str, float]:
            voltage = current_state["voltage"]
            d_voltage = -(voltage / (resistance * capacitance))
            next_voltage = voltage + (d_voltage * dt)

            return {"voltage": next_voltage}

        return step

    if problem.problem_type == "cooling_problem":
        ambient_temp = float(parameters["ambient_temp"])
        cooling_rate = float(parameters["cooling_rate"])

        def step(current_state: dict[str, float], dt: float) -> dict[str, float]:
            temperature = current_state["temperature"]
            d_temperature = -cooling_rate * (temperature - ambient_temp)
            next_temperature = temperature + (d_temperature * dt)

            return {"temperature": next_temperature}

        return step

    raise ValueError(f"Unsupported simulation problem_type: {problem.problem_type}")


def _build_stop_condition(
    problem: StructuredProblem,
) -> Callable[[dict[str, float], float], bool] | None:
    stop_at_ground = problem.simulation_config.get("stop_at_ground", False)

    if problem.problem_type == "projectile_problem_with_drag" and stop_at_ground:
        def stop_condition(current_state: dict[str, float], current_time: float) -> bool:
            return current_time > 0.0 and current_state["y"] <= 0.0

        return stop_condition

    return None


def _solve_with_monte_carlo(problem: StructuredProblem) -> dict[str, object]:
    config = problem.simulation_config
    trial_count = int(config.get("trial_count", 100))
    uncertain_parameters = config.get("uncertain_parameters", {})

    def sample_builder() -> StructuredProblem:
        sampled_problem = deepcopy(problem)

        for name, spec in uncertain_parameters.items():
            base_value = float(problem.parameters[name])
            spread = float(spec.get("spread", 0.0))
            sampled_problem.parameters[name] = random.uniform(
                base_value - spread,
                base_value + spread,
            )

        sampled_problem.simulation_config = {
            **sampled_problem.simulation_config,
            "use_monte_carlo": False,
        }
        return sampled_problem

    def trial_runner(sampled_problem: StructuredProblem) -> object:
        return solve_simulation_problem(sampled_problem)

    def aggregator(results: list[object]) -> dict[str, object]:
        return {
            "trial_count": len(results),
            "trials": results,
        }

    return run_monte_carlo(
        trial_count=trial_count,
        sample_builder=sample_builder,
        trial_runner=trial_runner,
        aggregator=aggregator,
    )
