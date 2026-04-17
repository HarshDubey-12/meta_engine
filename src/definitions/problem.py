"""Problem structure definitions."""
# Future changes:
# - Add stricter validation for StructuredProblem once parser examples stabilize.
# - Add Quantity/State schemas if dictionaries become too loose for solver inputs.
# - Replace free-form input_type/domain strings with enums if values stabilize.

# Importing utilities 
from dataclasses import dataclass, field

# Defining the dataclass for the raw problem definitions.
@dataclass
class RawProblem:
    """Raw problem definition should be 
    1> raw_content
        text/equation/data
    2> input_type
        text/equation/data/image 
    3> domain
        mechanics etc
    4> constraints
        initial conditions 
        assumptions
    5> metadata
        id 
        timestamp 
    """
    raw_content: str
    input_type: str
    domain: str | None = None
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)

@dataclass
class StructuredProblem:
    """Structured Problem Definitions include
    1> Initial States 
        Describing the initial state of the problem. 
        Text/Equation/Data
    2> Parameters
        What parameters the problem depends on.
        Text/Equation/Data
    3> Constraints 
        Limitations of the problem.
        Text/Equation
    4> Problem Type
        Text
    5> Output Type 
        Text/Equation/Data/Image(visualization)/Numbers  
    """
    problem_type: str
    output_type: str
    domain: str | None = None
    source_problem: RawProblem | None = None
    initial_state: dict[str, object] = field(default_factory=dict)
    parameters: dict[str, object] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
