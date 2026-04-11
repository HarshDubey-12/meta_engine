"""Feature schema definitions."""
# importing utilities 
from dataclasses import dataclass, field
from enum import Enum

# Defining Enums 
class DependencyType(Enum):
    UNKNOWN = "Unknown"
    NONE = "None"
    TIME = "Time"
    SPACE = "Space"
    TIME_AND_SPACE = "Time_and_space"

class MathematicalNature(Enum):
    UNKNOWN = "Unknown"
    LINEAR = "Linear"
    NONLINEAR = "Nonlinear"

class RepresentationType(Enum):
    UNKNOWN = "Unknown"
    TEXT = "Text"
    EQUATION = "Equation"
    DATA = "Data"
    MIXED =  "Mixed"

# Defining problem features.
@dataclass
class ProblemFeatures:
    """
    Problem features : Quantities derived from the problem statement
    1> known_variables 
    2> unknown_variables 
    3> dependency_type 
        time
        space 
        etc...
    4> mathematical_nature 
        linear 
        non_linear 
    5> variable_count
    6> representation_type 
        equation based 
        data based 
    """
    known_variables : list[str]=field(default_factory=list) 
    unknown_variables : list[str]=field(default_factory=list)
    dependency_type : DependencyType = DependencyType.UNKNOWN
    mathematical_nature : MathematicalNature = MathematicalNature.UNKNOWN
    variable_count : int=0
    representation_type : RepresentationType = RepresentationType.UNKNOWN