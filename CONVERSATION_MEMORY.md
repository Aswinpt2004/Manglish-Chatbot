# 💬 Conversation Memory System

## Overview
The Conversation Memory System stores message history per user and provides context to improve chatbot responses. This enables the bot to understand follow-up questions and maintain conversation continuity.

## Features

✅ **Per-User Conversation History**
- Stores complete message history for each user
- JSON file storage in `data/conversations/`

✅ **Context-Aware Responses**
- Passes recent conversation history to chatbot
- Improves understanding of follow-up questions
- Maintains conversational flow

✅ **Automatic History Management**
- Keeps last 20 messages per user (configurable)
- Auto-deletes messages older than 7 days
- Lightweight and efficient storage

✅ **Conversation Analytics**
- Track total messages, user vs bot
- View conversation timeline
- Average response length metrics

✅ **CLI Management Tool**
- List all users with conversations
- View conversation history
- Export conversations to JSON
- Clear individual or all conversations

## File Structure

```
data/
├── conversations/              # Conversation storage
│   ├── 918891381713.json      # One file per user
│   ├── 82592254705895.json
│   └── ...
```

## Usage

### Automatic (WhatsApp Bot)
Conversations are **automatically stored** when the bot receives and sends messages. No configuration needed!

### Manual (CLI Commands)

List all users with stored conversations:
```bash
node conversation_cli.js list
```

View conversation for a specific user:
```bash
node conversation_cli.js view 918891381713
```

Show statistics for a user:
```bash
node conversation_cli.js stats 918891381713
```

Export conversation as JSON file:
```bash
node conversation_cli.js export 918891381713
```

Clear conversation for a user:
```bash
node conversation_cli.js clear 918891381713
```

Clear ALL conversations (with confirmation):
```bash
node conversation_cli.js purge
```

## Configuration

Edit these constants in `conversationManager.js`:

```javascript
const MAX_HISTORY_PER_USER = 20;      // Keep last 20 messages
const HISTORY_EXPIRY_DAYS = 7;        // Delete messages older than 7 days
```

## Data Structure

Each conversation file contains:
```json
{
  "userId": "918891381713",
  "createdAt": "2026-01-08T10:30:00.000Z",
  "updatedAt": "2026-01-08T11:45:30.000Z",
  "messages": [
    {
      "timestamp": "2026-01-08T10:30:15.000Z",
      "role": "user",
      "content": "Vanakkam!",
      "intent": "greeting"
    },
    {
      "timestamp": "2026-01-08T10:30:18.000Z",
      "role": "assistant",
      "content": "Vanakkam! Epd iruko?",
      "intent": "greeting"
    }
  ]
}
```

## How It Works

### Step 1: User Sends Message
```
User: "Namaskaram!"
```

### Step 2: Load Recent History
Bot loads last 5 messages from `data/conversations/918891381713.json`

### Step 3: Create Context String
```
Previous conversation:
User: "Epd iruko?"
Bot: "Naan seri irukken..."
User: "Namaskaram!"
```

### Step 4: Send to Chatbot
Chatbot receives message + context for better understanding

### Step 5: Store Both Messages
- User message → saved with timestamp
- Bot response → saved with intent

## Example Workflow

**Message 1:**
```
User: "What's the weather?"
Bot: "I don't have access to weather data"
```

**Message 2:**
```
User: "Is it going to rain today?"  ← Follow-up question
Bot: [Understands context from previous msg]
    "I mentioned I can't access weather. Let me help with something else?"
```

## API (JavaScript)

### Load Conversation
```javascript
const conversation = ConversationManager.loadConversation(userId);
```

### Add Message
```javascript
ConversationManager.addMessage(userId, 'user', 'Hello!');
ConversationManager.addMessage(userId, 'assistant', 'Hi there!', 'greeting');
```

### Get Context
```javascript
const context = ConversationManager.getContext(userId, 5);
// Returns: { userId, messageCount, recentMessages, summary }
```

### Get Statistics
```javascript
const stats = ConversationManager.getStats(userId);
// Returns: { totalMessages, userMessages, botMessages, avgResponseLength, ... }
```

### Clear Conversation
```javascript
ConversationManager.clearConversation(userId);
```

### Export Conversation
```javascript
const data = ConversationManager.exportConversation(userId);
```

## Privacy Notes

⚠️ **Data Storage**: Conversations are stored locally in `data/conversations/` directory
- No data is sent to external servers
- User data can be deleted anytime using CLI
- Consider adding encryption for sensitive data

## Performance Impact

- **Storage**: ~500 bytes per message average
- **Memory**: Minimal (only loaded when needed)
- **Speed**: No noticeable impact on response time

## Troubleshooting

**Q: Where are conversations stored?**
A: In `data/conversations/` directory (created automatically)

**Q: How do I delete a conversation?**
A: Use `node conversation_cli.js clear <userId>`

**Q: Can I export conversations?**
A: Yes, use `node conversation_cli.js export <userId>`

**Q: How long are conversations kept?**
A: 7 days by default (configurable in conversationManager.js)

**Q: Does this slow down the bot?**
A: No, minimal performance impact

## Future Enhancements

- [ ] Database integration (SQLite/MongoDB)
- [ ] Encrypted storage for privacy
- [ ] Advanced analytics dashboard
- [ ] Conversation summarization
- [ ] Multi-language support analysis
- [ ] User sentiment tracking
- [ ] Intent-based conversation clustering
