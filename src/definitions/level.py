"""Problem level definitions."""
# Future changes:
# - Add Level 4+ when PDE, inverse, multi-physics, or ML-augmented systems are implemented.
# - Keep this file as the official level vocabulary; mapping rules belong in decision/mapper.py.
# - Add descriptions only if UI, docs, or logging need human-readable level explanations.

# Importing Utlities 
from enum import Enum

# Defining enum 
class ComplexityLevel(Enum):
    UNKNOWN = "unknown"
    LEVEL_0 = "direct_formula"
    LEVEL_1 = "multi_step_analytical"
    LEVEL_2 = "calculus_simple_ode"
    LEVEL_3 = "dynamic_simulation"
