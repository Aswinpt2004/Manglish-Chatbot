# 🚀 Quick Start Guide - Manglish Chatbot

This guide will help you get started with the Manglish Chatbot in just a few minutes!

## ⚡ Fast Setup (5 minutes)

### 1. Activate Virtual Environment

Your virtual environment is already created. Just activate it:

```powershell
.\chatbot\Scripts\Activate
```

You should see `(chatbot)` before your command prompt.

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the Complete Demo

```powershell
python demo.py
```

This will:
- ✅ Check all dependencies
- ✅ Preprocess your WhatsApp chat
- ✅ Analyze intents and patterns
- ✅ Start an interactive chatbot session

---

## 📝 Step-by-Step Usage

### Option A: Use Existing WhatsApp Data

You already have a WhatsApp chat file! Just run:

**Step 1: Preprocess the data**
```powershell
python preprocess_whatsapp.py
```

This will:
- Parse 68,000+ lines of WhatsApp chat
- Clean and normalize Manglish text
- Create conversation pairs
- Generate statistics
- Save processed data to `data/processed/`

**Step 2: Analyze intents (optional)**
```powershell
python intent_analyzer.py
```

This will:
- Analyze word and bigram frequency
- Cluster conversations by intent
- Generate intent-specific datasets
- Save analysis to `data/intents/`

**Step 3: Run the chatbot**
```powershell
python manglish_chatbot.py
```

Start chatting in Manglish!

### Option B: Use Built-in Patterns Only

If you don't want to use WhatsApp data, you can still use the chatbot with built-in intent patterns:

```powershell
python manglish_chatbot.py
```

The chatbot will use predefined patterns for:
- Greetings (hi, entha, sukham)
- Food (kazhicho, vishakkund)
- Study (assignment, exam, record)
- Time (eppo, neram)
- And more!

---

## 💬 Example Conversations

Try these inputs:

### Greetings
```
You: hi entha vishesham
Bot: Hey! Sukhamano?

You: sukhamano
Bot: Nalla sukham! Ningal?
```

### Food
```
You: food kazhicho
Bot: Vishakkano? Entha kazhikkan ulla?

You: biriyani kazhikanam
Bot: Pwoli food! Evidennu kittum?
```

### Study
```
You: assignment complete aayo
Bot: Assignment kazhinjoo?

You: illa ini cheyyanam
Bot: Alla? Pinne enthu?
```

### Mixed Language
```
You: exam eppozhanu
Bot: Padikkanam! Exam ethrayanu?

You: record work kazhinju
Bot: Record work complete aayo?
```

---

## 📊 Understanding the Output

### Preprocessing Output

After running `preprocess_whatsapp.py`, you'll get:

```
data/processed/
├── conversation_pairs.json    # Training data (context → response pairs)
├── conversation_pairs.csv     # Same data in CSV format
├── cleaned_messages.json      # All cleaned messages
└── dataset_statistics.json    # Dataset statistics
```

**Statistics include:**
- Total messages and conversation pairs
- Unique senders
- Word frequency
- Manglish percentage
- Top common words

### Intent Analysis Output

After running `intent_analyzer.py`, you'll get:

```
data/intents/
├── greeting_examples.json     # Greeting conversations
├── food_examples.json         # Food-related conversations
├── study_examples.json        # Study-related conversations
├── affirmation_examples.json  # Yes/OK responses
├── negation_examples.json     # No/Negation responses
├── word_frequency.json        # Top 200 words
└── bigram_frequency.json      # Top 100 two-word phrases
```

---

## 🎯 Chatbot Response Types

The chatbot uses a hybrid approach:

### 1. Intent-Based (Rule-Based)
```
You: hello
Bot: Hey! Sukhamano?
[Intent: greeting]
```

### 2. Similarity-Based (Data-Driven)
```
You: assignment kazhinjo
Bot: <Response from similar conversation in training data>
[Intent: similarity_0.87]
```

### 3. Fallback
```
You: [something unclear]
Bot: Mm... Manasilayilla! Vere reethiyil parayamo?
[Intent: fallback]
```

---

## 🔧 Customization

### Add New Intent

Edit `manglish_chatbot.py`, add to `_load_intent_patterns()`:

```python
'new_intent': {
    'patterns': [
        r'\b(keyword1|keyword2)\b',
        r'\b(phrase)\b'
    ],
    'responses': [
        "Response 1",
        "Response 2"
    ]
}
```

### Change Context Window

Edit `preprocess_whatsapp.py`:

```python
# Change from 1 to 2 or 3 for more context
preprocessor.create_conversation_pairs(context_window=2)
```

### Adjust Similarity Threshold

Edit `manglish_chatbot.py`:

```python
# Change threshold (0.0 to 1.0)
# Higher = stricter matching
similar_responses, score = self.find_similar_context(text_clean, threshold=0.7)
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'pandas'"
**Solution:** Install dependencies
```powershell
pip install -r requirements.txt
```

### Issue: "No conversation pairs generated"
**Solution:** Check WhatsApp chat format
- File should be in `chats/WhatsApp Chat.txt`
- Export format: `DD/MM/YY, HH:MM am/pm - Name: Message`

### Issue: "Chatbot only gives fallback responses"
**Solution:** Run preprocessing first
```powershell
python preprocess_whatsapp.py
```

### Issue: "FileNotFoundError"
**Solution:** Make sure you're in the project directory
```powershell
cd d:\Chatbot_reborn
```

---

## 📈 Next Steps

1. **Experiment with the chatbot**
   - Try different Manglish phrases
   - Test mixed language inputs
   - See how it handles spelling variations

2. **Analyze your data**
   - Check `data/processed/dataset_statistics.json`
   - Review word frequency patterns
   - Identify common conversation topics

3. **Improve the chatbot**
   - Add more intents based on your data
   - Expand response variety
   - Fine-tune similarity threshold

4. **Advanced features**
   - Create a web interface
   - Add voice input/output
   - Integrate with messaging platforms
   - Train ML models for better understanding

---

## 📚 Files Overview

| File | Purpose |
|------|---------|
| `preprocess_whatsapp.py` | Parse and clean WhatsApp data |
| `manglish_chatbot.py` | Main chatbot engine |
| `intent_analyzer.py` | Analyze patterns and intents |
| `demo.py` | Run complete pipeline |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `QUICKSTART.md` | This file! |

---

## 🎓 Learning Path

**Beginner:**
1. Run the demo
2. Chat with the bot
3. Review generated statistics

**Intermediate:**
1. Understand preprocessing pipeline
2. Analyze intent patterns
3. Add custom intents

**Advanced:**
1. Modify similarity matching
2. Implement ML models
3. Build web interface
4. Deploy as service

---

## ✨ Tips for Best Results

1. **Use natural Manglish**: Type how you normally chat
   - ✅ "entha cheyyunne" (natural)
   - ❌ "what are you doing" (too formal)

2. **Mix languages freely**: The chatbot understands code-mixing
   - ✅ "food kazhicho? feeling hungry"
   - ✅ "assignment kazhinjo or not"

3. **Don't worry about spelling**: Multiple variations work
   - "entha" = "enthada" = "enthu" = "enta"
   - "illa" = "illya" = "ilya"

4. **Keep it conversational**: Chat like you're texting a friend
   - ✅ "yo entha plan today"
   - ✅ "mm ok sheri"

---

## 🚀 Ready to Start?

```powershell
# 1. Activate environment
.\chatbot\Scripts\Activate

# 2. Install dependencies
pip install pandas

# 3. Run preprocessing
python preprocess_whatsapp.py

# 4. Start chatting!
python manglish_chatbot.py
```

**Happy Chatting in Manglish! 🎉**

---

*For detailed documentation, see [README.md](README.md)*
