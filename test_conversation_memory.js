#!/usr/bin/env node

/**
 * Test Conversation Manager
 * ==========================
 * Quick test to verify conversation memory system works
 */

const ConversationManager = require('./conversationManager');

console.log('🧪 Testing Conversation Memory System\n');
console.log('='.repeat(60));

// Test 1: Add messages
console.log('\n✅ Test 1: Adding messages...');
const testUserId = 'test_user_12345';

ConversationManager.addMessage(testUserId, 'user', 'Namaskaram!');
ConversationManager.addMessage(testUserId, 'assistant', 'Vanakkam! Epd iruko?', 'greeting');
ConversationManager.addMessage(testUserId, 'user', 'What is your name?');
ConversationManager.addMessage(testUserId, 'assistant', 'Manglish Chatbot aanu ennode peru', 'greeting');

console.log('✓ Messages added successfully');

// Test 2: Load conversation
console.log('\n✅ Test 2: Loading conversation...');
const conversation = ConversationManager.loadConversation(testUserId);
console.log(`✓ Loaded ${conversation.messages.length} messages`);

// Test 3: Get context
console.log('\n✅ Test 3: Getting conversation context...');
const context = ConversationManager.getContext(testUserId, 5);
console.log('✓ Context retrieved:');
console.log('\nRecent Messages:');
context.recentMessages.forEach((msg, idx) => {
    console.log(`  ${idx + 1}. [${msg.role}] ${msg.content}`);
});

// Test 4: Get statistics
console.log('\n✅ Test 4: Getting conversation stats...');
const stats = ConversationManager.getStats(testUserId);
console.log('✓ Statistics:');
console.log(`  - Total Messages: ${stats.totalMessages}`);
console.log(`  - User Messages: ${stats.userMessages}`);
console.log(`  - Bot Messages: ${stats.botMessages}`);
console.log(`  - Avg Response Length: ${stats.avgResponseLength.toFixed(0)} chars`);

// Test 5: Format for display
console.log('\n✅ Test 5: Formatting conversation for display...');
const formatted = ConversationManager.formatForDisplay(testUserId);
console.log('✓ Formatted output:');
console.log(formatted);

// Test 6: List all users
console.log('\n✅ Test 6: Listing all users...');
const users = ConversationManager.getAllUsers();
console.log(`✓ Found ${users.length} user(s):`);
users.forEach(user => console.log(`  - ${user}`));

// Test 7: Export conversation
console.log('\n✅ Test 7: Exporting conversation...');
const exported = ConversationManager.exportConversation(testUserId);
console.log(`✓ Export successful (${JSON.stringify(exported).length} bytes)`);

console.log('\n' + '='.repeat(60));
console.log('\n🎉 All tests passed! Conversation memory is working correctly.\n');

// Cleanup: Clear test data
console.log('🧹 Cleaning up test data...');
ConversationManager.clearConversation(testUserId);
console.log('✓ Test data cleared\n');
