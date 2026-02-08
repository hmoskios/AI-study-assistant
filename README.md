# Engineering Study Assistant

A Streamlit-based AI study assistant designed to help engineering students understand problems and validate their reasoning using open-source large language models.

The app provides two core capabilities:
1. **Step-by-step explanations** of engineering problems
2. **Automated reasoning verification** that identifies mistakes and explains why they occur

---

## Features

- 🧠 **Explain Mode**
  - Generates clear, step-by-step explanations
  - Defines variables, shows units, and highlights common mistakes
  - Adjustable explanation depth (concise vs. detailed)

- ✅ **Verify My Reasoning**
  - Evaluates a student’s attempted solution
  - Flags the *first incorrect step*
  - Explains what was done well and what went wrong
  - Provides a corrected solution outline and sanity checks

- 🧼 **Clean, student-facing output**
  - No chain-of-thought leakage
  - Plain-text equations (no LaTeX clutter)
  - Consistent Markdown formatting

---

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **Ollama** (local LLM inference)
- **Open-source LLMs** (Hugging Face ecosystem, e.g. LLaMA-family models)
- **Git & GitHub** (version control)

---

## Why Local Inference?

The project initially explored hosted inference options, but ultimately uses **local inference via Ollama** to:
- Avoid API quotas and usage limits
- Enable unrestricted experimentation
- Better understand model behavior and formatting constraints
- Keep the project fully free to run

This design also demonstrates the ability to switch inference backends based on cost and reliability tradeoffs.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Ollama installed

### 1. Install Ollama and pull the model
```bash
ollama pull llama3.2
```

### 2. Install Python dependencies
```bash
pip install streamlit requests
```

### 3. Run the app
```bash
streamlit run app.py
```
The app will open automatically in your browser.


### Example Use Cases

* Understanding physics, statics, dynamics, or circuits problems
* Checking homework solutions for conceptual or algebraic mistakes
* Practicing step-by-step problem-solving with feedback