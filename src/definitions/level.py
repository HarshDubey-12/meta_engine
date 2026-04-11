"""Problem level definitions."""
# Importing Utlities 
from enum import Enum

# Defining enum 
class ComplexityLevel(Enum):
    UNKNOWN = "unknown"
    LEVEL_0 = "direct_formula"
    LEVEL_1 = "multi_step_analytical"
    LEVEL_2 = "calculus_simple_ode"
    LEVEL_3 = "dynamic_simulation"