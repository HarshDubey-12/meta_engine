"""Euler method implementation."""
def euler_integrate(
    derivative_function,
    initial_state: dict[str, float],
    start_time: float,
    end_time: float,
    dt: float,
) -> list[dict[str, float]]:
    """Apply Euler integration using a derivative function supplied by the model."""

    if dt <= 0:
        raise ValueError("dt must be positive.")

    if end_time <= start_time:
        raise ValueError("end_time should be after the start_time.")

    current_state = dict(initial_state)
    current_time = start_time

    trajectory = []

    initial_snapshot = {"time": current_time, **current_state}
    trajectory.append(initial_snapshot)

    while current_time < end_time:
        derivatives = derivative_function(current_time, current_state)

        next_state = {}

        for variable in current_state:
            derivative_value = derivatives[variable]
            next_state[variable] = current_state[variable] + derivative_value * dt

        current_time = current_time + dt

        snapshot = {"time": current_time, **next_state}
        trajectory.append(snapshot)

        current_state = next_state

    return trajectory
