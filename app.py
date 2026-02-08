import os
import re
import streamlit as st
from openai import OpenAI
import requests

# ----------------------------
# Setup
# ----------------------------
st.set_page_config(page_title="AI Study Assistant for Engineering Students", page_icon="📚", layout="centered")


# ----------------------------
# Helpers
# ----------------------------
def clean_output(text: str) -> str:
    # Strip any leaked chain-of-thought tags
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"


def llm_chat(system: str, user: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    raw = data["message"]["content"]
    return clean_output(raw)


def build_explain_system(tone: str) -> str:
    base = (
        "You are a patient engineering tutor. "
        "Explain step-by-step, define variables, show units when relevant, "
        "and point out common mistakes. "
        "If information is missing (diagram/values), ask for what’s needed.\n\n"
        "IMPORTANT RULES:\n"
        "- Do NOT include <think> or </think> tags\n"
        "- Do NOT show hidden reasoning\n"
        "- Use clean Markdown\n"
        "- Use normal equations inline (e.g., N = m*g*cos(theta))\n"
    )
    if tone == "Concise":
        return base + "\nKeep it short and focused. Prefer bullets.\n"
    if tone == "Detailed":
        return base + "\nBe more detailed and show intermediate steps.\n"
    return base


def explain(problem: str, topic: str, tone: str) -> str:
    system = build_explain_system(tone)
    user = (
        f"Topic: {topic}\n\n"
        f"Problem:\n{problem}\n\n"
        "Return format (use these headings):\n"
        "### Concept overview\n"
        "- 2–5 bullets\n\n"
        "### Step-by-step\n"
        "1. ...\n\n"
        "### Quick check\n"
        "- units / sign / reasonableness\n"
    )
    return llm_chat(system, user)


def verify(problem: str, attempt: str, strictness: str) -> str:
    system = (
        "You are a rigorous but kind engineering tutor.\n\n"
        "IMPORTANT RULES:\n"
        "- Do NOT include <think> or </think> tags\n"
        "- Do NOT show hidden reasoning\n"
        "- Use clean Markdown\n"
        "- Be precise and student-friendly\n"
        "- Identify the FIRST incorrect step and why\n"
        "- Do NOT use LaTeX or backslashes (no \\theta, \\text{}, \\approx, etc.)\n"
        "- Use normal equations inline (e.g., N = m*g*cos(theta))\n"
    )

    if strictness == "Strict":
        system += "\nBe strict: treat missing units/justifications as issues.\n"
    else:
        system += "\nBe supportive: focus on major conceptual/math errors first.\n"

    user = (
        f"Problem:\n{problem}\n\n"
        f"Student attempt:\n{attempt}\n\n"
        "Output format (use these exact headings):\n"
        "### Verdict\n"
        "One of: Correct / Partially correct / Incorrect / Insufficient information\n\n"
        "### What you did well\n"
        "- bullets\n\n"
        "### Where it goes wrong\n"
        "- bullets (include the first incorrect step and why)\n\n"
        "### Corrected solution outline\n"
        "1. numbered steps (not overly long)\n\n"
        "### Quick sanity check\n"
        "- units / sign / reasonableness\n"
    )
    return llm_chat(system, user)


# ----------------------------
# UI
# ----------------------------
st.title("📚 AI Study Assistant for Engineering Students")
st.caption("Explain problems step-by-step and verify your reasoning.")

with st.sidebar:
    st.subheader("Settings")
    topic = st.selectbox(
        "Topic",
        ["General", "Calculus", "Physics", "Statics", "Dynamics", "Circuits", "Materials", "Thermo"],
        index=0,
    )
    tone = st.radio("Explanation detail", ["Balanced", "Concise", "Detailed"], index=0)
    strictness = st.radio("Verification style", ["Supportive", "Strict"], index=0)
    st.divider()
    st.write("**Model:**", OLLAMA_MODEL)
    st.write("Tip: Keep your question self-contained (givens, diagram description, what to solve for).")

tab_explain, tab_verify = st.tabs(["🧠 Explain", "✅ Verify my reasoning"])

with tab_explain:
    st.subheader("Explain a problem")
    problem = st.text_area(
        "Paste the problem here:",
        height=180,
        placeholder="Example: A 2 kg block slides down a 30° incline with μ=0.2. Find the acceleration.",
        key="problem_explain",
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        explain_btn = st.button("Generate explanation", use_container_width=True)
    with col2:
        st.write("")  # spacer

    if explain_btn:
        if not problem.strip():
            st.warning("Please paste a problem first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = explain(problem, topic, tone)
                    st.markdown(answer)
                except Exception as e:
                    st.error("Request failed.")
                    st.code(str(e))


with tab_verify:
    st.subheader("Verify your attempt")
    problem_v = st.text_area(
        "Paste the problem here:",
        height=140,
        placeholder="Paste the same problem statement here.",
        key="problem_verify",
    )
    attempt = st.text_area(
        "Paste your attempt / reasoning here:",
        height=220,
        placeholder="Paste what you tried (equations, steps, assumptions).",
        key="attempt_verify",
    )

    verify_btn = st.button("Verify my reasoning", use_container_width=True)

    if verify_btn:
        if not problem_v.strip():
            st.warning("Please paste the problem first.")
        elif not attempt.strip():
            st.warning("Please paste your attempt so I can verify it.")
        else:
            with st.spinner("Checking your reasoning..."):
                try:
                    report = verify(problem_v, attempt, strictness)
                    st.markdown(report)
                except Exception as e:
                    st.error("Request failed.")
                    st.code(str(e))
