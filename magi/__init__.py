"""
MAGI Supercomputer System
=========================

S.C. MAGI (マギ) System - A trio of multipurpose supercomputers designed by 
Dr. Naoko Akagi during her research into bio-computers at Gehirn.

The MAGI's 7th generation organic computers are implanted with three differing 
aspects of Dr. Naoko Akagi's personality using the Personality Transplant OS:

- MELCHIOR (MAGI-1): Her persona as a scientist
- BALTHASAR (MAGI-2): Her persona as a mother  
- CASPER (MAGI-3): Her persona as a woman

Architecture:
- Personality Transplant OS (PTOS): Core personality encoding technology
- Organic Processor: 7th generation bio-neural computing substrate
- Memory Engrams: Persistent associative memory structures
- Consensus Protocol: Multi-unit voting and deliberation system
- MAGI Network: Global network connecting replica installations
- MAGI Achiral: Modular rack-based system (Rebuild continuity)

Known MAGI Installations:
- MAGI-01: Tokyo-3, Japan (Original - NERV HQ)
- MAGI-02: Matsushiro, Japan
- MAGI-03: Berlin, Germany
- MAGI-04: Massachusetts, USA
- MAGI-05: Hamburg, Germany
- MAGI-06: Beijing, China
"""

# Core decision engine
from .core.engine import MAGIEngine
from .core.brain import Brain
from .core.personality import Personality
from .core.decision import Decision, Verdict, DeliberationRound

# PTOS - Personality Transplant Operating System
from .ptos.matrix import PersonalityMatrix, PersonalityAspect, PersonalityFragment
from .ptos.organic import OrganicProcessor, ProcessingMode
from .ptos.transplant import TransplantProcedure, TransplantResult
from .ptos.engram import MemoryEngram, EngramStore, EngramType

# The Three MAGI Units
from .brains import MELCHIOR, BALTHASAR, CASPER

# Network and Consensus
from .network.system import MAGISystem, MAGIUnit, SystemStatus
from .network.consensus import ConsensusProtocol, VotingSession, ConsensusResult
from .network.network import MAGINetwork, NetworkNode, IntrusionDetector
from .network.achiral import MAGIAchiral, AchiralBank, AchiralModule

# LLM Integration
from .llm.client import create_openai_client

__version__ = "2.0.0"
__codename__ = "NERV"

__all__ = [
    # Core
    "MAGIEngine",
    "Brain", 
    "Personality",
    "Decision",
    "Verdict",
    "DeliberationRound",
    
    # PTOS
    "PersonalityMatrix",
    "PersonalityAspect",
    "PersonalityFragment",
    "OrganicProcessor",
    "ProcessingMode",
    "TransplantProcedure",
    "TransplantResult",
    "MemoryEngram",
    "EngramStore",
    "EngramType",
    
    # Brains
    "MELCHIOR",
    "BALTHASAR", 
    "CASPER",
    
    # System
    "MAGISystem",
    "MAGIUnit",
    "SystemStatus",
    
    # Consensus
    "ConsensusProtocol",
    "VotingSession",
    "ConsensusResult",
    
    # Network
    "MAGINetwork",
    "NetworkNode",
    "IntrusionDetector",
    
    # Achiral
    "MAGIAchiral",
    "AchiralBank",
    "AchiralModule",
    
    # LLM
    "create_openai_client",
]
