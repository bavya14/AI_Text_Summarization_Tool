# BrieflyAI — AI Text Summarization Tool

BrieflyAI is an interactive web app that creates concise summaries of long text using a pretrained transformer summarization model. It is designed as an educational Natural Language Processing (NLP) project.

## Features

- Paste text or load a built-in example
- Generate short, balanced, or detailed summaries
- View word count, character count, and estimated reading time
- Edit the generated summary in the app
- Download the result as a `.txt` file
- Splits longer text into manageable chunks
- No API key required

## Tech stack

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- DistilBART summarization model: `sshleifer/distilbart-cnn-12-6`

## Project structure

```text
AI_Text_Summarization_Tool/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── sample_documents/
│   └── README.md
└── tests/
    └── README.md
```

## Requirements

- Python 3.10–3.12 recommended
- Internet access for the first model download
- Several GB of free disk space may be needed for PyTorch and model dependencies
- A CPU can run the model, but summarization may take time

## Run locally

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/AI_Text_Summarization_Tool.git
cd AI_Text_Summarization_Tool
```

### 2. Create a virtual environment

**Windows:**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

The first summary may take longer while the model is downloaded and loaded.

## How it works

1. The user pastes a passage or loads the sample.
2. The app normalizes whitespace and calculates basic text statistics.
3. The text is split into chunks if necessary.
4. The pretrained DistilBART model generates summaries for the chunks.
5. The user can review, edit, and download the result.

## Important limitations

- Summaries may omit details, change emphasis, or occasionally contain inaccurate information.
- Results depend on source length, language, and writing style.
- The selected model is primarily intended for English text.
- This app is a learning demonstration, not a substitute for reading or verifying important legal, medical, academic, or financial material.
- The model is downloaded from Hugging Face the first time it runs; after download, inference can run locally.

## GitHub upload

Create a repository named `AI_Text_Summarization_Tool`. Extract the project ZIP and upload the contents of the project folder, not the ZIP itself.

Or use Git:

```bash
git init
git add .
git commit -m "Add BrieflyAI text summarization tool"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI_Text_Summarization_Tool.git
git push -u origin main
```

## License

MIT License. See `LICENSE`.
