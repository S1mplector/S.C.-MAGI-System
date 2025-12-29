"""
MAGI Supercomputer System
=========================

A sophisticated decision-making engine inspired by the MAGI system from Evangelion.
Three distinct AI personalities deliberate and reach consensus on complex questions.

The system implements:
- Three unique brain instances (Melchior, Balthasar, Casper)
- Multi-round deliberation with cross-examination
- Weighted voting with confidence scores
- Consensus synthesis and conflict resolution
"""

from .core.engine import MAGIEngine
from .core.brain import Brain
from .core.personality import Personality
from .core.decision import Decision, Verdict, DeliberationRound
from .brains import MELCHIOR, BALTHASAR, CASPER

__version__ = "2.0.0"
__all__ = [
    "MAGIEngine",
    "Brain", 
    "Personality",
    "Decision",
    "Verdict",
    "DeliberationRound",
    "MELCHIOR",
    "BALTHASAR", 
    "CASPER",
]
