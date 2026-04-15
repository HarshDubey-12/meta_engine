"""Select the computational model for a problem."""
# Future changes:
# - Use ProblemFeatures along with ComplexityLevel for more accurate model selection.
# - Same level does not always imply the same model: Level 2 + linear may use an analytical shortcut,
#   while Level 2 + nonlinear may need an ODE solver.
# - Introduce a full Strategy pattern later with a shared selector interface and swappable selectors
#   such as RuleBasedSelector, MLBasedSelector, CostAwareSelector, or AccuracyFirstSelector.
# - Move ModelType to a shared definitions module if dispatcher, runner, logger, and tests all depend on it.

from enum import Enum
from src.definitions.level import ComplexityLevel

class ModelType(Enum):
    UNKNOWN = "unknown"
    ANALYTICAL = "analytical"
    SYMBOLIC = "symbolic"
    ODE = "ode"
    SIMULATION = "simulation" 

# Implementing rule based model selection using strategy pattern.
def select_model_for_level(complexity: ComplexityLevel) -> ModelType:
    # safety check
    if complexity is None:
        return ModelType.UNKNOWN
    
    if complexity == ComplexityLevel.LEVEL_0:
        return ModelType.ANALYTICAL

    if complexity ==ComplexityLevel.LEVEL_1:
        return ModelType.SYMBOLIC

    if complexity ==ComplexityLevel.LEVEL_2:
        return ModelType.ODE

    if complexity ==ComplexityLevel.LEVEL_3:
        return ModelType.SIMULATION

    # Fallback
    return ModelType.UNKNOWN
