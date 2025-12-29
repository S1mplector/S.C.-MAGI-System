"""
MAGI AI Module
==============

Bridge module providing backward compatibility with the original interface
while using the new MAGI engine architecture under the hood.

This module is kept for compatibility with main.py callbacks.
The new architecture lives in the magi/ package.
"""

from magi.api import (
    is_yes_or_no_question,
    get_answer,
    classify_answer,
    MAGISystem,
    MAGIResponse
)

__all__ = [
    "is_yes_or_no_question",
    "get_answer", 
    "classify_answer",
    "MAGISystem",
    "MAGIResponse"
]
