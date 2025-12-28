/**
 * WhatsApp Bot using Node.js
 * ===========================
 * Connects Manglish Chatbot to WhatsApp using whatsapp-web.js
 * Handles QR code authentication and automatic responses
 * 
 * Author: Chatbot_reborn Project
 * Date: December 2025
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { spawn } = require('child_process');

// ============================================
// CONFIGURATION
// ============================================
const ALLOWED_CONTACTS = [
    'Aswin P.T',
    'Aswin P. T',
    '918891381713',  // Phone number (fallback when contact name unavailable)
    // Add more contact names here
];

const CHECK_INTERVAL = 5000; // Check every 5 seconds
const RESPOND_TO_ALL = false; // Set to true to respond to everyone

// ============================================
// WhatsApp Client Setup
// ============================================
const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "manglish-chatbot"
    }),
    puppeteer: {
        headless: true,
        executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-web-security'
        ]
    }
});

// ============================================
// Chatbot Response Generator
// ============================================
async function getChatbotResponse(message) {
    return new Promise((resolve, reject) => {
        // Call Python chatbot to generate response
        const python = spawn('python', ['-c', `
import sys
import os
import json

# Set UTF-8 encoding for Windows console
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from manglish_chatbot import ManglishChatbot

chatbot = ManglishChatbot(conversation_data_path='data/processed/conversation_pairs.json', quiet=True)
user_input = sys.argv[1]
response, intent = chatbot.generate_response(user_input)
result = {"response": response, "intent": intent}
print(json.dumps(result, ensure_ascii=False))
`, message], {
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
        });

        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
        });

        python.stderr.on('data', (data) => {
            error += data.toString();
        });

        python.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python error: ${error}`));
            } else {
                try {
                    // Get only the last line (JSON output), ignore debug prints
                    const lines = output.trim().split('\n');
                    const jsonLine = lines[lines.length - 1];
                    const result = JSON.parse(jsonLine);
                    resolve(result);
                } catch (e) {
                    reject(new Error(`Failed to parse response: ${output}`));
                }
            }
        });
    });
}

// ============================================
// Contact Filter
// ============================================
function isContactAllowed(contactName) {
    if (RESPOND_TO_ALL) {
        return true;
    }
    return ALLOWED_CONTACTS.includes(contactName);
}

// ============================================
// Event Handlers
// ============================================

// QR Code for authentication
client.on('qr', (qr) => {
    console.log('\n' + '='.repeat(60));
    console.log('📱 SCAN THIS QR CODE WITH YOUR PHONE');
    console.log('='.repeat(60));
    console.log('');
    
    // Display QR code in terminal
    qrcode.generate(qr, { small: true });
    
    console.log('');
    console.log('📲 Steps to scan:');
    console.log('   1. Open WhatsApp on your phone');
    console.log('   2. Go to Settings → Linked Devices');
    console.log('   3. Tap "Link a Device"');
    console.log('   4. Scan the QR code above');
    console.log('='.repeat(60));
    console.log('');
});

// Authentication successful
client.on('authenticated', () => {
    console.log('✅ Authentication successful!');
});

// Ready to receive messages
client.on('ready', () => {
    console.log('\n' + '='.repeat(60));
    console.log('🤖 WhatsApp Manglish Chatbot is READY!');
    console.log('='.repeat(60));
    
    if (RESPOND_TO_ALL) {
        console.log('⚠️  Mode: Responding to ALL contacts');
    } else {
        console.log('📋 Allowed contacts:');
        ALLOWED_CONTACTS.forEach(contact => {
            console.log(`   - ${contact}`);
        });
    }
    
    console.log('\n⏳ Waiting for messages...');
    console.log('Press Ctrl+C to stop the bot\n');
    console.log('='.repeat(60) + '\n');
});

// Handle incoming messages
client.on('message', async (msg) => {
    try {
        // Get contact info with fallback; suppress noisy library errors
        let contactName = 'Unknown';
        const safeGetContact = async () => {
            try {
                const contact = await msg.getContact();
                return contact;
            } catch (e) {
                return null;
            }
        };
        const contact = await safeGetContact();
        contactName = (contact && (contact.pushname || contact.name || contact.number)) || msg.from.replace('@c.us', '') || 'Unknown';
        
        // Skip messages from self
        if (msg.fromMe) {
            return;
        }
        
        // Skip group messages and broadcast/status updates
        if (msg.from.includes('@g.us') || msg.from === 'status@broadcast') {
            return;
        }
        
        // Check if contact is allowed
        if (!isContactAllowed(contactName)) {
            console.log(`🚫 Skipping message from: ${contactName} (not in allowed list)`);
            return;
        }
        
        console.log(`\n💬 Message from: ${contactName}`);
        console.log(`   User: ${msg.body}`);
        
        // Get chatbot response
        try {
            const result = await getChatbotResponse(msg.body);
            console.log(`   Bot: ${result.response} [Intent: ${result.intent}]`);
            
            // Send response
            await msg.reply(result.response);
            console.log('   ✅ Response sent\n');
            
        } catch (error) {
            console.error(`   ❌ Error generating response: ${error.message}`);
            
            // Send fallback message
            await msg.reply('Mm... Manasilayilla! Vere reethiyil parayamo?');
            console.log('   ⚠️  Sent fallback response\n');
        }
        
    } catch (error) {
        console.error('❌ Error processing message:', error.message);
    }
});

// Authentication failure
client.on('auth_failure', (msg) => {
    console.error('❌ Authentication failed:', msg);
    console.log('\n💡 Try deleting .wwebjs_auth folder and run again');
});

// Disconnected
client.on('disconnected', (reason) => {
    console.log('\n⚠️  WhatsApp disconnected:', reason);
    console.log('💡 Restart the bot to reconnect\n');
});

// ============================================
// Start the bot
// ============================================
async function startBot() {
    try {
        console.log('\n🚀 Starting WhatsApp Bot...');
        console.log('⏳ Initializing browser and connecting to WhatsApp...\n');
        
        // Add event listener for initialization start
        client.on('loading_screen', (percent, message) => {
            console.log(`📊 ${message} - ${percent}%`);
        });
        
        // Set timeout for initialization
        const initTimeout = setTimeout(() => {
            console.log('⏱️  Still initializing... this may take a minute on first run');
            console.log('   (Browser is being set up)\n');
        }, 15000);
        
        await client.initialize();
        clearTimeout(initTimeout);
        
        console.log('\n✅ Bot initialized successfully\n');
    } catch (error) {
        console.error('\n❌ Failed to start bot');
        console.error('Error Message:', error.message);
        console.error('Error Stack:', error.stack);
        console.error('\n💡 Troubleshooting:');
        console.error('   1. Delete .wwebjs_auth folder and try again');
        console.error('   2. Make sure WhatsApp is not already open in another session');
        console.error('   3. Check that Edge browser is installed correctly\n');
        
        try {
            await client.destroy();
        } catch (e) {
            // Ignore destroy errors
        }
        process.exit(1);
    }
}

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n\n⏹️  Stopping bot...');
    try {
        await client.destroy();
        console.log('✅ Bot stopped\n');
    } catch (error) {
        console.error('Error stopping bot:', error);
    }
    process.exit(0);
});

// Handle uncaught errors
process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Rejection:', reason);
});

process.on('uncaughtException', (error) => {
    console.error('❌ Uncaught Exception:', error.message);
});

// Start the bot
startBot();
