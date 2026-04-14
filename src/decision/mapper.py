"""Map extracted features to problem levels."""
# Future changes:
# - Replace simple if/else heuristics with configurable rules or a strategy object as complexity grows.
# - Use richer analyzer features, such as equation_count or requires_iteration, to reduce weak guesses.
# - Keep this file responsible only for feature-to-level mapping, not model selection or execution.

from src.definitions.features import ProblemFeatures, DependencyType, MathematicalNature, RepresentationType
from src.definitions.level import ComplexityLevel

def map_features_to_level(features: ProblemFeatures) -> ComplexityLevel:
    "maps extracted problem to a level."

    # Safety Check
    if features is None:
        return ComplexityLevel.UNKNOWN
    
    # Rule 1: Dynamic Simulation problems (highest complexity)
    if features.dependency_type == DependencyType.TIME_AND_SPACE and features.mathematical_nature == MathematicalNature.NONLINEAR:
        return ComplexityLevel.LEVEL_3
    
    # Rule 2: Calculus/ODE problems 
    if features.dependency_type == DependencyType.TIME:
        return ComplexityLevel.LEVEL_2
    
    # Rule 3: multivariable analytical problems 
    if features.representation_type == RepresentationType.EQUATION and features.variable_count>3 :
        return ComplexityLevel.LEVEL_1
    
    # Rule 4: Direct formula problems
    if features.representation_type in (RepresentationType.TEXT, RepresentationType.EQUATION):
        return ComplexityLevel.LEVEL_0
    
    # Fallback
    return ComplexityLevel.UNKNOWN
