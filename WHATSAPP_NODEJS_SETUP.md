# WhatsApp Bot Setup - Node.js Version

## 🚀 Quick Start Guide

This is a **much more reliable** WhatsApp integration using Node.js instead of Python Selenium.

---

## 📋 Prerequisites

### 1. Install Node.js
Download and install Node.js (v16 or higher): https://nodejs.org/

**Verify installation:**
```powershell
node --version
npm --version
```

---

## 🔧 Installation Steps

### Step 1: Install Dependencies
```powershell
npm install
```

This will install:
- `whatsapp-web.js` - Official WhatsApp Web API wrapper
- `qrcode-terminal` - Display QR code in terminal

### Step 2: Configure Allowed Contacts
Open `whatsapp_bot.js` and edit the configuration:

```javascript
const ALLOWED_CONTACTS = [
    'Aswin P.T',
    'Aswin P. T',
    // Add more contact names here
];
```

**To respond to everyone:**
```javascript
const RESPOND_TO_ALL = true;
```

---

## ▶️ Running the Bot

### Start the bot:
```powershell
npm start
```

OR

```powershell
node whatsapp_bot.js
```

### What happens next:

1. **QR Code appears in terminal** - automatically!
2. **Scan with your phone:**
   - Open WhatsApp
   - Settings → Linked Devices
   - Link a Device
   - Scan the QR code
3. **Bot is ready!** - Starts responding to messages automatically

---

## 🎯 Features

✅ **QR code in terminal** - No browser needed!  
✅ **Session persistence** - Scan once, stays logged in  
✅ **Automatic message detection** - Works perfectly  
✅ **Contact filtering** - Respond only to specific people  
✅ **Uses your Python chatbot** - Calls manglish_chatbot.py for responses  
✅ **No Selenium issues** - Much more stable  

---

## 🛑 Stopping the Bot

Press `Ctrl + C` in the terminal

---

## 📝 Configuration Options

### Change Check Interval
```javascript
const CHECK_INTERVAL = 5000; // milliseconds (5 seconds)
```

### Allow/Block Groups
By default, groups are blocked. To enable:

In `whatsapp_bot.js`, comment out this section:
```javascript
// Skip group messages (optional - uncomment to allow groups)
// if (msg.from.includes('@g.us')) {
//     return;
// }
```

---

## 🧹 Reset Session

If you need to scan QR code again:

```powershell
# Delete session folder
Remove-Item -Recurse -Force .wwebjs_auth -ErrorAction SilentlyContinue

# Run bot again
npm start
```

---

## 🔍 Troubleshooting

### "Python not found"
Make sure Python is in your PATH and `manglish_chatbot.py` exists.

### QR Code not showing
- Check your internet connection
- Make sure Node.js is installed correctly
- Try: `npm install` again

### "Module not found"
```powershell
npm install
```

### Authentication fails
```powershell
Remove-Item -Recurse -Force .wwebjs_auth
npm start
```

### Bot not responding
- Check that contact names match exactly
- Look at terminal for error messages
- Verify Python chatbot works: `python -c "from manglish_chatbot import ManglishChatbot; print('OK')"`

---

## 📊 Monitoring

The terminal shows:
- ✅ Messages received
- 🤖 Bot responses generated
- 🎯 Intent detected
- ❌ Any errors

Example output:
```
💬 Message from: Aswin P.T
   User: Hi entha vishesham
   Bot: Hey! Sukhamano? [Intent: greeting]
   ✅ Response sent
```

---

## 🆚 Why Node.js is Better

| Feature | Python (Selenium) | Node.js |
|---------|------------------|---------|
| QR Code | Browser window | Terminal |
| Reliability | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup | Complex | Simple |
| Resources | High | Low |
| Session | Often breaks | Stable |

---

## 🔐 Security Notes

- Session data stored in `.wwebjs_auth/`
- Add to `.gitignore` if using git:
  ```
  .wwebjs_auth/
  node_modules/
  ```

---

## 🚀 Running 24/7

### Using PM2 (Process Manager):
```powershell
npm install -g pm2
pm2 start whatsapp_bot.js --name whatsapp-bot
pm2 save
pm2 startup
```

### View logs:
```powershell
pm2 logs whatsapp-bot
```

### Stop:
```powershell
pm2 stop whatsapp-bot
```

---

## 📚 Additional Resources

- [whatsapp-web.js Documentation](https://wwebjs.dev/)
- [Node.js Documentation](https://nodejs.org/docs/)

---

**Enjoy your stable WhatsApp bot! 🤖💬**
