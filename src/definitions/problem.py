"""Problem structure definitions."""
# Future changes:
# - Add StructuredProblem when parser output needs a formal contract.
# - Replace free-form input_type/domain strings with enums if values stabilize.
# - Add validation only after real parser examples show what rules are needed.

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
        timestamp """
    
    raw_content: str
    input_type: str
    domain: str | None = None
    constraints: list[str]=field(default_factory = list)
    metadata: dict[str, object]=field(default_factory = dict)
