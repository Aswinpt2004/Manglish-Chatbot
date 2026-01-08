/**
 * Conversation Memory Manager
 * ==========================
 * Stores and retrieves conversation history per user
 * Maintains context for better response generation
 * 
 * Author: Chatbot_reborn Project
 * Date: January 2026
 */

const fs = require('fs');
const path = require('path');

const CONVERSATIONS_DIR = path.join(__dirname, 'data', 'conversations');
const MAX_HISTORY_PER_USER = 20; // Keep last 20 messages
const HISTORY_EXPIRY_DAYS = 7; // Clear history older than 7 days

// Ensure conversations directory exists
if (!fs.existsSync(CONVERSATIONS_DIR)) {
    fs.mkdirSync(CONVERSATIONS_DIR, { recursive: true });
}

class ConversationManager {
    /**
     * Get conversation file path for a user
     */
    static getConversationPath(userId) {
        return path.join(CONVERSATIONS_DIR, `${userId}.json`);
    }

    /**
     * Load conversation history for a user
     */
    static loadConversation(userId) {
        try {
            const filePath = this.getConversationPath(userId);
            
            if (!fs.existsSync(filePath)) {
                return {
                    userId,
                    createdAt: new Date().toISOString(),
                    messages: []
                };
            }

            const data = fs.readFileSync(filePath, 'utf8');
            const conversation = JSON.parse(data);

            // Cleanup old messages
            conversation.messages = this.pruneOldMessages(conversation.messages);

            return conversation;
        } catch (error) {
            console.error(`❌ Error loading conversation for ${userId}:`, error.message);
            return {
                userId,
                createdAt: new Date().toISOString(),
                messages: []
            };
        }
    }

    /**
     * Save conversation history for a user
     */
    static saveConversation(userId, conversation) {
        try {
            const filePath = this.getConversationPath(userId);
            
            // Keep only recent messages
            if (conversation.messages.length > MAX_HISTORY_PER_USER) {
                conversation.messages = conversation.messages.slice(-MAX_HISTORY_PER_USER);
            }

            conversation.updatedAt = new Date().toISOString();
            fs.writeFileSync(filePath, JSON.stringify(conversation, null, 2), 'utf8');
        } catch (error) {
            console.error(`❌ Error saving conversation for ${userId}:`, error.message);
        }
    }

    /**
     * Add a message to conversation history
     */
    static addMessage(userId, role, content, intent = null) {
        const conversation = this.loadConversation(userId);
        
        conversation.messages.push({
            timestamp: new Date().toISOString(),
            role, // 'user' or 'assistant'
            content,
            intent // Store intent for analysis
        });

        this.saveConversation(userId, conversation);
        return conversation;
    }

    /**
     * Get conversation context (last N messages)
     */
    static getContext(userId, contextLength = 5) {
        const conversation = this.loadConversation(userId);
        
        if (conversation.messages.length === 0) {
            return null;
        }

        const recentMessages = conversation.messages.slice(-contextLength);
        return {
            userId,
            messageCount: conversation.messages.length,
            recentMessages,
            summary: this.generateContextSummary(recentMessages)
        };
    }

    /**
     * Generate a text summary of recent conversation
     */
    static generateContextSummary(messages) {
        if (messages.length === 0) return '';

        return messages
            .map(msg => `${msg.role === 'user' ? 'User' : 'Bot'}: ${msg.content}`)
            .join('\n');
    }

    /**
     * Remove old messages (older than HISTORY_EXPIRY_DAYS)
     */
    static pruneOldMessages(messages) {
        const expiryTime = new Date();
        expiryTime.setDate(expiryTime.getDate() - HISTORY_EXPIRY_DAYS);

        return messages.filter(msg => {
            const msgTime = new Date(msg.timestamp);
            return msgTime > expiryTime;
        });
    }

    /**
     * Clear conversation for a user
     */
    static clearConversation(userId) {
        try {
            const filePath = this.getConversationPath(userId);
            if (fs.existsSync(filePath)) {
                fs.unlinkSync(filePath);
                console.log(`✅ Conversation cleared for ${userId}`);
            }
        } catch (error) {
            console.error(`❌ Error clearing conversation for ${userId}:`, error.message);
        }
    }

    /**
     * Get all users with stored conversations
     */
    static getAllUsers() {
        try {
            const files = fs.readdirSync(CONVERSATIONS_DIR);
            return files
                .filter(file => file.endsWith('.json'))
                .map(file => file.replace('.json', ''));
        } catch (error) {
            console.error('❌ Error reading conversations directory:', error.message);
            return [];
        }
    }

    /**
     * Get conversation statistics
     */
    static getStats(userId) {
        const conversation = this.loadConversation(userId);
        const messages = conversation.messages;

        if (messages.length === 0) {
            return {
                userId,
                totalMessages: 0,
                userMessages: 0,
                botMessages: 0,
                avgResponseLength: 0,
                firstMessage: null,
                lastMessage: null
            };
        }

        const userMsgs = messages.filter(m => m.role === 'user');
        const botMsgs = messages.filter(m => m.role === 'assistant');

        return {
            userId,
            totalMessages: messages.length,
            userMessages: userMsgs.length,
            botMessages: botMsgs.length,
            avgResponseLength: botMsgs.reduce((sum, m) => sum + m.content.length, 0) / (botMsgs.length || 1),
            firstMessage: messages[0].timestamp,
            lastMessage: messages[messages.length - 1].timestamp
        };
    }

    /**
     * Export conversation as JSON
     */
    static exportConversation(userId) {
        const conversation = this.loadConversation(userId);
        return conversation;
    }

    /**
     * Format conversation for display
     */
    static formatForDisplay(userId, limit = 10) {
        const conversation = this.loadConversation(userId);
        const messages = conversation.messages.slice(-limit);

        return messages
            .map(msg => ({
                time: new Date(msg.timestamp).toLocaleTimeString(),
                role: msg.role === 'user' ? '👤' : '🤖',
                text: msg.content,
                intent: msg.intent || '-'
            }))
            .map(m => `[${m.time}] ${m.role} ${m.text}${m.intent !== '-' ? ` [${m.intent}]` : ''}`)
            .join('\n');
    }
}

module.exports = ConversationManager;
