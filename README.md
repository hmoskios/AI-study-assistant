# AI Study Assistant

A Streamlit-based AI study assistant designed to help engineering students understand problems and validate their reasoning using open-source large language models.

The app provides two core capabilities:
1. **Step-by-step explanations** of engineering problems.
2. **Automated reasoning verification** that identifies mistakes and explains how to fix them.

---

## Features

- **Explain Mode:**
  - Generates clear, step-by-step explanations.
  - Defines variables, shows units, and highlights common mistakes.
  - Adjustable explanation depth (concise vs. detailed).

- **Verify My Reasoning:**
  - Evaluates a student’s attempted solution.
  - Flags the first incorrent step.
  - Explains what was done well and what went wrong.
  - Provides a corrected solution outline and sanity checks.

- **Subject Selection:**
  - Allows students to choose from a variety of engineering topics, including as calculus, physics, statics, dynamics, circuits, materials, and thermo.

- **Well-Formatted, Easy-to-Read Responses:**
  - No chain-of-thought leakage.
  - Markdown formatting.

---

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **Ollama** (local LLM inference)
- **Open-Source LLMs** (llama3.2)

---

## Why Local Inference?

The project initially explored hosted inference options, but ultimately uses **local inference via Ollama** to:
- Avoid API quotas and usage limits
- Enable unrestricted experimentation
- Keep the project fully free to run

This design also has the ability to easily switch inference backends based on cost and reliability tradeoffs.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Ollama installed

### 1. Clone the Repository
```bash
git clone https://github.com/hmoskios/AI-study-assistant.git
cd AI-study-assistant
```

### 2. Pull the Model
```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```
The app will open automatically in your browser.
