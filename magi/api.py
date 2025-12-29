"""
MAGI API
========

High-level API for the MAGI system, providing simple functions
for the Dash application to interact with the decision engine.
"""

from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
import threading

from .core.engine import MAGIEngine, EngineConfig
from .core.brain import Brain, BrainConfig
from .core.decision import Decision, VerdictType
from .brains import create_melchior, create_balthasar, create_casper
from .llm.client import create_openai_client


@dataclass
class MAGIResponse:
    """Response from the MAGI system for UI consumption."""
    status: str  # "yes", "no", "conditional", "info", "error", "deadlock"
    answer: str
    question_type: str
    consensus: str
    
    # Individual brain responses
    melchior: Dict[str, Any]
    balthasar: Dict[str, Any]
    casper: Dict[str, Any]
    
    # Metadata
    decision_id: str
    processing_time_ms: float


class MAGISystem:
    """
    Singleton-style MAGI system manager.
    
    Provides a simple interface for the Dash application while
    managing the underlying engine and brains.
    """
    
    _instance: Optional["MAGISystem"] = None
    _lock = threading.Lock()
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self._api_key = api_key
        self._model = model
        self._engine: Optional[MAGIEngine] = None
        self._initialized = False
    
    @classmethod
    def get_instance(cls) -> "MAGISystem":
        """Get or create the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def initialize(self, api_key: str, model: str = "gpt-4") -> None:
        """Initialize or reinitialize the MAGI system with an API key."""
        self._api_key = api_key
        self._model = model
        
        # Create LLM client
        client = create_openai_client(api_key=api_key)
        
        # Create brain configuration
        brain_config = BrainConfig(model=model)
        
        # Create the three brains
        melchior = create_melchior(brain_config)
        balthasar = create_balthasar(brain_config)
        casper = create_casper(brain_config)
        
        # Create engine configuration
        engine_config = EngineConfig(
            model=model,
            max_deliberation_rounds=2,
            enable_cross_examination=True,
            parallel_processing=True
        )
        
        # Create the engine
        self._engine = MAGIEngine(
            brains=[melchior, balthasar, casper],
            config=engine_config,
            llm_client=client
        )
        
        self._initialized = True
    
    @property
    def is_initialized(self) -> bool:
        return self._initialized and self._engine is not None
    
    def deliberate(self, question: str) -> MAGIResponse:
        """
        Run full MAGI deliberation on a question.
        
        Returns a MAGIResponse suitable for UI consumption.
        """
        if not self.is_initialized:
            raise RuntimeError("MAGI system not initialized. Call initialize() first.")
        
        try:
            decision = self._engine.deliberate(question)
            return self._decision_to_response(decision)
        except Exception as e:
            return MAGIResponse(
                status="error",
                answer=str(e),
                question_type="unknown",
                consensus="error",
                melchior={"status": "error", "response": str(e), "conditions": None},
                balthasar={"status": "error", "response": str(e), "conditions": None},
                casper={"status": "error", "response": str(e), "conditions": None},
                decision_id="error",
                processing_time_ms=0.0
            )
    
    def _decision_to_response(self, decision: Decision) -> MAGIResponse:
        """Convert a Decision to a MAGIResponse."""
        
        def brain_to_dict(name: str) -> Dict[str, Any]:
            if name not in decision.final_verdicts:
                return {
                    "status": "info",
                    "response": "No response",
                    "conditions": None
                }
            
            verdict = decision.final_verdicts[name]
            return {
                "status": decision.get_brain_status(name),
                "response": verdict.reasoning,
                "summary": verdict.summary,
                "confidence": verdict.confidence,
                "conditions": verdict.conditions if verdict.conditions else None,
                "reservations": verdict.reservations if verdict.reservations else None
            }
        
        return MAGIResponse(
            status=decision.status,
            answer=decision.final_answer,
            question_type=decision.question_type,
            consensus=decision.consensus_type.value,
            melchior=brain_to_dict("melchior"),
            balthasar=brain_to_dict("balthasar"),
            casper=brain_to_dict("casper"),
            decision_id=decision.id,
            processing_time_ms=decision.processing_time_ms
        )
    
    def get_brain_response(self, brain_name: str, question: str) -> str:
        """Get a direct response from a specific brain."""
        if not self.is_initialized:
            raise RuntimeError("MAGI system not initialized.")
        
        return self._engine.get_brain_response(brain_name, question)


# Convenience functions for backward compatibility with old ai.py interface

_magi_system = MAGISystem.get_instance()


def is_yes_or_no_question(question: str, key: str) -> bool:
    """
    Determine if a question is a yes/no question.
    
    Backward compatible with old ai.py interface.
    """
    if not _magi_system.is_initialized:
        _magi_system.initialize(api_key=key)
    
    try:
        client = create_openai_client(api_key=key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": 'You classify questions. Answer with ONLY "yes" or "no". Is this a yes/no question (can it be answered with yes or no)?'},
                {"role": "user", "content": question}
            ],
            max_tokens=5,
            temperature=0.0
        )
        
        content = response.choices[0].message.content.strip().lower()
        return content.startswith("yes")
        
    except Exception:
        return False


def get_answer(question: str, personality: str, key: str) -> str:
    """
    Get an answer from a MAGI brain based on personality description.
    
    Backward compatible with old ai.py interface.
    """
    # Map old personality strings to brain names
    brain_name = None
    personality_lower = personality.lower()
    
    if "scientist" in personality_lower:
        brain_name = "melchior"
    elif "mother" in personality_lower:
        brain_name = "balthasar"
    elif "woman" in personality_lower:
        brain_name = "casper"
    
    if not _magi_system.is_initialized:
        _magi_system.initialize(api_key=key)
    
    if brain_name:
        return _magi_system.get_brain_response(brain_name, question)
    
    # Fallback: use the engine directly
    client = create_openai_client(api_key=key)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a MAGI supercomputer. {personality}"},
            {"role": "user", "content": question}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content


def classify_answer(question: str, personality: str, answer: str, key: str) -> Dict[str, Any]:
    """
    Classify an answer as yes/no/conditional.
    
    Backward compatible with old ai.py interface.
    """
    client = create_openai_client(api_key=key)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a MAGI supercomputer. {personality}"},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
            {"role": "user", "content": 'Summarize your answer with a simple "yes" or "no" (one word). If not possible, list conditions under which the answer would be "yes".'}
        ],
        max_tokens=200,
        temperature=0.3
    )
    
    content = response.choices[0].message.content.strip().lower()
    
    import re
    if re.match(r'^\W*yes\W*$', content, re.IGNORECASE):
        return {'status': 'yes', 'conditions': None}
    
    if re.match(r'^\W*no\W*$', content, re.IGNORECASE):
        return {'status': 'no', 'conditions': None}
    
    return {'status': 'conditional', 'conditions': content}
