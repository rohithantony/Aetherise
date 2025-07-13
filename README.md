# 🌍 Aetherise — Climate Education Chatbot

Aetherise is a modern, interactive chatbot built using Streamlit that educates users on climate change. With a clean, dynamic interface and fuzzy question matching, Aetherise helps users learn about environmental issues, trusted sources, and important facts.

## 🚀 Features

- 💬 Ask natural language questions about climate change
- 🎯 Fuzzy matching with a curated dataset of Q&A
- 🔗 Topic-based trusted resource links
- 🌿 Climate facts & suggestions panel
- ✨ Stylish interface with animated side panels
- 📂 Data-driven via Excel (editable)

## 📁 File Structure

```

aetherise/
├── aetherise\_app.py                  # Streamlit application file
├── Climate\_Change\_Chatbot\_Questions.xlsx  # Dataset with questions, answers, links
├── requirements.txt                  # Project dependencies
└── README.md                         # You're reading it!

````

## 🧠 Dataset Format

The Excel file must contain columns:
- `question`
- `answer`
- `topic`
- `trusted links`

Each row represents a question-answer pair with associated metadata.

## 📦 Installation

```bash
git clone https://github.com/your-username/Aetherise.git
cd Aetherise
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

## ▶️ Run the App

```bash
streamlit run aetherise_app.py
```

## 🌐 Live Demo (Optional)

Coming soon via Streamlit Community Cloud!

## 🙌 Credits

Built with 💚 by [Rohith Antony](https://github.com/rohithantony)

---

Stay informed. Stay green. 🌱

```
