"""
MAGI Brains
===========

The three MAGI supercomputer personalities, each representing
a distinct aspect of Dr. Naoko Akagi's psyche.
"""

from .melchior import MELCHIOR, create_melchior
from .balthasar import BALTHASAR, create_balthasar
from .casper import CASPER, create_casper

__all__ = [
    "MELCHIOR",
    "BALTHASAR", 
    "CASPER",
    "create_melchior",
    "create_balthasar",
    "create_casper",
]
