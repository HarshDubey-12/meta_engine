from src.decision.model_selector import ModelType, select_model_for_level
from src.definitions.level import ComplexityLevel


def test_model_selector_returns_ode_for_level_2() -> None:
    model_type = select_model_for_level(ComplexityLevel.LEVEL_2)

    assert model_type == ModelType.ODE
