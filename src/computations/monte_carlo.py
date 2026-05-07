"""Monte Carlo computation primitives."""
from collections.abc import Callable


def run_monte_carlo(
    trial_count: int,
    sample_builder: Callable[[], object],
    trial_runner: Callable[[object], object],
    aggregator: Callable[[list[object]], object] | None = None,
) -> object:
    """Run repeated randomized trials and optionally aggregate results."""
    if trial_count <= 0:
        raise ValueError("trial_count must be positive.")

    results: list[object] = []

    for _ in range(trial_count):
        sample = sample_builder()
        result = trial_runner(sample)
        results.append(result)

    if aggregator is not None:
        return aggregator(results)

    return results
