#!/usr/bin/env node

/**
 * Conversation Manager CLI
 * =======================
 * Manage conversation history from command line
 * 
 * Usage:
 *   node conversation_cli.js list                - List all users
 *   node conversation_cli.js view <userId>       - View conversation for user
 *   node conversation_cli.js stats <userId>      - Show stats for user
 *   node conversation_cli.js clear <userId>      - Clear conversation for user
 *   node conversation_cli.js export <userId>     - Export conversation as JSON
 *   node conversation_cli.js purge               - Clear all conversations
 */

const ConversationManager = require('./conversationManager');
const fs = require('fs');
const path = require('path');

const command = process.argv[2];
const userId = process.argv[3];

console.log('📝 Conversation Manager CLI\n');

switch (command) {
    case 'list':
        handleList();
        break;
    case 'view':
        handleView(userId);
        break;
    case 'stats':
        handleStats(userId);
        break;
    case 'clear':
        handleClear(userId);
        break;
    case 'export':
        handleExport(userId);
        break;
    case 'purge':
        handlePurge();
        break;
    default:
        showHelp();
}

// ============================================
// Command Handlers
// ============================================

function handleList() {
    console.log('📋 All Users with Conversations:\n');
    const users = ConversationManager.getAllUsers();
    
    if (users.length === 0) {
        console.log('   No conversations found.');
        return;
    }
    
    users.forEach((user, index) => {
        const stats = ConversationManager.getStats(user);
        console.log(`   ${index + 1}. ${user}`);
        console.log(`      Messages: ${stats.totalMessages} (User: ${stats.userMessages}, Bot: ${stats.botMessages})`);
        console.log(`      Last: ${new Date(stats.lastMessage).toLocaleString()}`);
    });
    console.log(`\nTotal users: ${users.length}`);
}

function handleView(userId) {
    if (!userId) {
        console.error('❌ Please provide a user ID');
        process.exit(1);
    }
    
    console.log(`📖 Conversation History for ${userId}:\n`);
    const formatted = ConversationManager.formatForDisplay(userId, 50);
    
    if (formatted.length === 0) {
        console.log('   No messages found.');
        return;
    }
    
    console.log(formatted);
}

function handleStats(userId) {
    if (!userId) {
        console.error('❌ Please provide a user ID');
        process.exit(1);
    }
    
    console.log(`📊 Statistics for ${userId}:\n`);
    const stats = ConversationManager.getStats(userId);
    
    console.log(`   Total Messages: ${stats.totalMessages}`);
    console.log(`   User Messages: ${stats.userMessages}`);
    console.log(`   Bot Messages: ${stats.botMessages}`);
    console.log(`   Avg Bot Response Length: ${stats.avgResponseLength.toFixed(0)} chars`);
    console.log(`   First Message: ${new Date(stats.firstMessage).toLocaleString()}`);
    console.log(`   Last Message: ${new Date(stats.lastMessage).toLocaleString()}`);
}

function handleClear(userId) {
    if (!userId) {
        console.error('❌ Please provide a user ID');
        process.exit(1);
    }
    
    ConversationManager.clearConversation(userId);
    console.log(`✅ Conversation cleared for ${userId}`);
}

function handleExport(userId) {
    if (!userId) {
        console.error('❌ Please provide a user ID');
        process.exit(1);
    }
    
    const conversation = ConversationManager.exportConversation(userId);
    const filename = `conversation_export_${userId}_${Date.now()}.json`;
    
    fs.writeFileSync(filename, JSON.stringify(conversation, null, 2), 'utf8');
    console.log(`✅ Conversation exported to: ${filename}`);
}

function handlePurge() {
    console.warn('⚠️  This will delete ALL conversations. Type "yes" to confirm:');
    
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    rl.question('> ', (answer) => {
        if (answer.toLowerCase() === 'yes') {
            const users = ConversationManager.getAllUsers();
            users.forEach(user => {
                ConversationManager.clearConversation(user);
            });
            console.log(`✅ All ${users.length} conversations cleared.`);
        } else {
            console.log('❌ Cancelled.');
        }
        rl.close();
    });
}

function showHelp() {
    console.log(`
🎯 Available Commands:

   list              - List all users with stored conversations
   view <userId>     - View full conversation for a user
   stats <userId>    - Show conversation statistics
   clear <userId>    - Clear conversation for a user
   export <userId>   - Export conversation to JSON file
   purge             - Clear all conversations (confirmation required)

Examples:
   node conversation_cli.js list
   node conversation_cli.js view 918891381713
   node conversation_cli.js stats 918891381713
   node conversation_cli.js export 918891381713
    `);
}
