# MAGI

MAGI system is a cluster of three AI supercomputers that manage and support all tasks performed by the NERV organization from their Tokyo-3 headquarters.

Originally designed by Dr. Naoko Akagi, each of the three AI agents reflects a separate part of her complex personality:
- **MELCHIOR • 1** - The Scientist: analytical, empirical, truth-seeking
- **BALTHASAR • 2** - The Mother: protective, nurturing, compassionate  
- **CASPER • 3** - The Woman: passionate, freedom-seeking, meaning-driven

These often conflicting yet complementary agents participate in a sophisticated deliberation process to answer humanity's most challenging questions.

<p align="center">
  <img src="https://raw.githubusercontent.com/TomaszRewak/MAGI/master/examples/example_1.gif" width=800/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/TomaszRewak/MAGI/master/examples/example_2.gif" width=800/>
</p>

## Architecture (v2.0)

The MAGI system has been completely refactored with a sophisticated decision engine:

```
magi/
├── core/
│   ├── engine.py      # MAGIEngine - orchestrates deliberation
│   ├── brain.py       # Brain - individual supercomputer unit
│   ├── personality.py # Personality - psychological profiles
│   └── decision.py    # Decision, Verdict, Consensus types
├── brains/
│   ├── melchior.py    # The Scientist personality
│   ├── balthasar.py   # The Mother personality
│   └── casper.py      # The Woman personality
├── llm/
│   └── client.py      # Modern OpenAI API integration
└── api.py             # High-level API for applications
```

### Key Features

- **Multi-round Deliberation**: Brains engage in multiple rounds, considering each other's positions
- **Cross-examination**: Each brain critically examines the others' arguments
- **Weighted Voting**: Verdicts include confidence scores for nuanced consensus
- **Rich Personalities**: Deep psychological profiles with values, biases, and cognitive styles
- **Consensus Synthesis**: Intelligent synthesis of agreements and disagreements

### Deliberation Process

1. **Question Classification**: Determine question type (yes/no, open, analytical, ethical, predictive)
2. **Independent Analysis**: Each brain analyzes from its unique perspective
3. **Initial Verdicts**: Each brain forms an independent position with confidence level
4. **Cross-examination**: Brains examine and respond to each other's positions
5. **Updated Verdicts**: Positions refined after considering other arguments
6. **Consensus Synthesis**: Final decision with agreements, disagreements, and conditions

### Consensus Types

- **UNANIMOUS** (合意) - All three brains agree
- **MAJORITY** - Two brains agree, one dissents
- **CONDITIONAL** (状態) - Agreement with conditions attached
- **DEADLOCK** - No clear majority reached
- **INFORMATIONAL** (情報) - Non-decision question answered

### Brain Personalities

**MELCHIOR (The Scientist)**
- Cognitive Style: Analytical
- Primary Values: Truth, Knowledge, Progress, Objectivity
- Strengths: Rigorous logic, synthesizing complex information, long-term thinking
- Blindspots: May undervalue emotional or intuitive considerations

**BALTHASAR (The Mother)**
- Cognitive Style: Empathetic
- Primary Values: Protection, Wellbeing, Compassion, Safety
- Strengths: Understanding emotional needs, protecting the vulnerable, generational thinking
- Blindspots: May be overprotective, slow to accept necessary risks

**CASPER (The Woman)**
- Cognitive Style: Intuitive
- Primary Values: Freedom, Self-actualization, Love, Meaning
- Strengths: Understanding motivation, creative solutions, enabling flourishing
- Blindspots: May underestimate practical constraints, romanticize risk

## Usage

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/TomaszRewak/MAGI.git
cd MAGI

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Set API key (recommended)
export OPENAI_API_KEY="your-api-key"

# Start the server
python main.py
```

Navigate to http://127.0.0.1:8050/ in your browser.

### Programmatic Usage

```python
from magi import MAGIEngine
from magi.brains import MELCHIOR, BALTHASAR, CASPER
from magi.llm import create_openai_client

# Create the engine
client = create_openai_client(api_key="your-key")
engine = MAGIEngine(
    brains=[MELCHIOR, BALTHASAR, CASPER],
    llm_client=client
)

# Run deliberation
decision = engine.deliberate("Should humanity pursue interstellar travel?")

print(f"Consensus: {decision.consensus_type.value}")
print(f"Final verdict: {decision.final_verdict.value}")
print(f"Synthesis: {decision.synthesis}")

# Access individual brain positions
for name, verdict in decision.final_verdicts.items():
    print(f"{name}: {verdict.summary} (confidence: {verdict.confidence:.0%})")
```

## License

MIT License
