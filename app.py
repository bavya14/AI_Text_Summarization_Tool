import re
from pathlib import Path

import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="BrieflyAI | Text Summarizer", page_icon="📝", layout="wide")

st.markdown("""
<style>
.main-title {font-size:2.3rem;font-weight:750;margin-bottom:.1rem}
.subtitle {color:#6b7280;margin-bottom:1.2rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📝 BrieflyAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Turn long text into a shorter, easier-to-read summary using an NLP model.</div>',
    unsafe_allow_html=True,
)

st.info(
    "This app uses a pretrained summarization model. The first run downloads model files, "
    "so it needs internet access and may take several minutes."
)

with st.sidebar:
    st.header("Summary settings")
    summary_style = st.radio("Summary length", ["Short", "Balanced", "Detailed"], index=1)
    st.caption("These settings control the target summary length, not a guaranteed word count.")
    st.divider()
    st.markdown("### Model")
    st.caption("sshleifer/distilbart-cnn-12-6")
    st.markdown("### Tech stack")
    st.caption("Python · Streamlit · Hugging Face Transformers")

TARGETS = {
    "Short": (25, 60),
    "Balanced": (50, 110),
    "Detailed": (80, 160),
}
MAX_INPUT_CHARS = 18000

@st.cache_resource(show_spinner="Loading summarization model…")
def load_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        device=-1,
    )

def clean_text(text: str) -> str:
    """Normalize whitespace without changing the meaning of the input."""
    return re.sub(r"\s+", " ", text).strip()

def split_into_chunks(text: str, max_chars: int = 2800):
    """Split long input at sentence boundaries when possible."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for sentence in sentences:
        if not sentence:
            continue
        if len(sentence) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(sentence), max_chars):
                chunks.append(sentence[start:start + max_chars])
            continue
        candidate = f"{current} {sentence}".strip()
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks

sample_text = (
    "Artificial intelligence is changing how people work, learn, and communicate. "
    "Natural language processing helps computers analyze and generate human language. "
    "Text summarization is an NLP task that creates a shorter version of a document while "
    "preserving its most important information. Extractive methods select existing sentences "
    "from the source, while abstractive methods generate new wording. Modern transformer "
    "models can produce fluent summaries, but their output should be checked for missing "
    "details or unsupported claims. Summarization can help students review notes, help "
    "professionals scan reports, and help readers understand lengthy articles more quickly. "
    "The quality of a summary depends on the source text, model, and chosen length."
)

st.subheader("Enter your text")
input_mode = st.radio("Input method", ["Paste text", "Use sample text"], horizontal=True)
if input_mode == "Use sample text":
    text_input = st.text_area("Text to summarize", value=sample_text, height=250)
else:
    text_input = st.text_area(
        "Text to summarize",
        height=250,
        placeholder="Paste an article, study notes, report, or other text here...",
    )

normalized = clean_text(text_input)
words = re.findall(r"\b[\w'-]+\b", normalized)
col1, col2, col3 = st.columns(3)
col1.metric("Words", f"{len(words):,}")
col2.metric("Characters", f"{len(normalized):,}")
col3.metric("Estimated reading time", f"{max(1, round(len(words) / 200))} min" if words else "—")

if len(normalized) > MAX_INPUT_CHARS:
    st.warning(f"For this demo, please keep the input under {MAX_INPUT_CHARS:,} characters.")

if st.button("Generate summary", type="primary", use_container_width=True):
    if not normalized:
        st.warning("Please enter or select some text first.")
    elif len(normalized) < 80:
        st.warning("Please provide a longer passage (at least 80 characters) for a useful summary.")
    elif len(normalized) > MAX_INPUT_CHARS:
        st.error("The input is too long for this demo. Shorten it and try again.")
    else:
        min_len, max_len = TARGETS[summary_style]
        chunks = split_into_chunks(normalized)
        try:
            summarizer = load_summarizer()
            summaries = []
            with st.spinner("Summarizing your text…"):
                for chunk in chunks:
                    chunk_words = len(chunk.split())
                    # Avoid asking the model for more output tokens than the source can support.
                    local_max = min(max_len, max(20, int(chunk_words * 0.8)))
                    local_min = min(min_len, max(8, local_max - 10))
                    if chunk_words < 35:
                        summaries.append(chunk)
                    else:
                        result = summarizer(
                            chunk,
                            max_length=local_max,
                            min_length=local_min,
                            do_sample=False,
                            truncation=True,
                        )
                        summaries.append(result[0]["summary_text"].strip())

            final_summary = " ".join(summaries).strip()
            st.divider()
            st.subheader("Generated summary")
            st.text_area("Review and edit your summary", value=final_summary, height=220)
            st.download_button(
                "Download summary (.txt)",
                data=final_summary,
                file_name="brieflyai_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.caption(
                "AI-generated summaries can omit nuance or introduce errors. Verify important "
                "facts against the original text."
            )
        except Exception as exc:
            st.error("Could not generate a summary. Check your internet connection and try again.")
            with st.expander("Technical details"):
                st.code(str(exc))

st.divider()
st.markdown(
    "<div style='text-align:center;color:#6b7280;font-size:.85rem;'>"
    "BrieflyAI · Educational NLP project</div>",
    unsafe_allow_html=True,
)
