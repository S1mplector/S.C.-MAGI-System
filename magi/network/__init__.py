"""
MAGI Network
============

The global network of MAGI systems, including the original Tokyo-3 system
and replica installations worldwide.

Known MAGI installations:
- MAGI 01: Tokyo-3, Japan (Original - NERV HQ)
- MAGI 02: Matsushiro, Japan
- MAGI 03: Berlin, Germany
- MAGI 04: Massachusetts, USA
- MAGI 05: Hamburg, Germany
- MAGI 06: Beijing, China

This module also implements the MAGI Achiral - the modular rack-based
system developed for the AAA Wunder, consisting of countless modules
each containing three smaller computing units.
"""

from .system import MAGISystem, MAGIUnit, SystemStatus
from .consensus import ConsensusProtocol, VotingSession, ConsensusResult
from .network import MAGINetwork, NetworkNode, ConnectionStatus
from .achiral import MAGIAchiral, AchiralModule, AchiralBank

__all__ = [
    "MAGISystem",
    "MAGIUnit", 
    "SystemStatus",
    "ConsensusProtocol",
    "VotingSession",
    "ConsensusResult",
    "MAGINetwork",
    "NetworkNode",
    "ConnectionStatus",
    "MAGIAchiral",
    "AchiralModule",
    "AchiralBank",
]
