"""
WhatsApp Chat Data Preprocessor for Manglish Chatbot
=====================================================
This script preprocesses WhatsApp chat export data to create a clean dataset
for training a Manglish (Malayalam-English) chatbot.

Features:
- Extracts messages from WhatsApp export format
- Removes system messages, media notifications, deleted messages
- Cleans and normalizes Manglish text
- Creates conversation pairs for training
- Generates statistics about the dataset
"""

import re
import json
import pandas as pd
from datetime import datetime
from collections import Counter
import os


class WhatsAppPreprocessor:
    """Preprocessor for WhatsApp chat exports"""
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.messages = []
        self.conversation_pairs = []
        self.stats = {}
        
    def parse_whatsapp_chat(self):
        """Parse WhatsApp chat export file"""
        print(f"📂 Loading chat from: {self.input_file}")
        
        # WhatsApp message pattern: DD/MM/YY, HH:MM [am/pm] - Name: Message
        pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m)\s-\s([^:]+):\s(.+)'
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = re.findall(pattern, content)
        
        for timestamp, sender, message in matches:
            # Skip system messages and media
            if self._is_valid_message(message):
                self.messages.append({
                    'timestamp': timestamp,
                    'sender': sender.strip(),
                    'message': message.strip()
                })
        
        print(f"✅ Parsed {len(self.messages)} valid messages")
        return self.messages
    
    def _is_valid_message(self, message):
        """Check if message is valid for training"""
        # Filter out system messages, media, and deleted messages
        invalid_patterns = [
            '<Media omitted>',
            'deleted this message',
            'Messages and calls are end-to-end encrypted',
            'changed the subject',
            'changed this group',
            'added',
            'removed',
            'left',
            'joined using this group',
            'https://',
            'http://'
        ]
        
        for pattern in invalid_patterns:
            if pattern.lower() in message.lower():
                return False
        
        # Check if message has meaningful content
        if len(message.strip()) < 2:
            return False
            
        return True
    
    def clean_text(self, text):
        """Clean and normalize Manglish text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep Manglish-friendly punctuation
        text = re.sub(r'[^\w\s\.\?\!,\'\-]', '', text)
        
        # Normalize repeated characters (e.g., "yessss" -> "yes")
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        
        # Convert to lowercase for consistency
        text = text.lower()
        
        return text.strip()
    
    def create_conversation_pairs(self, context_window=1):
        """
        Create conversation pairs from messages
        context_window: number of previous messages to consider as context
        """
        print(f"🔄 Creating conversation pairs with context window={context_window}...")
        
        for i in range(context_window, len(self.messages)):
            # Get context (previous messages)
            context = []
            for j in range(i - context_window, i):
                context.append(self.messages[j]['message'])
            
            # Current message is the response
            response = self.messages[i]['message']
            
            # Clean messages
            context_clean = [self.clean_text(msg) for msg in context]
            response_clean = self.clean_text(response)
            
            # Skip if any message is too short after cleaning
            if all(len(msg) > 2 for msg in context_clean) and len(response_clean) > 2:
                self.conversation_pairs.append({
                    'context': context_clean,
                    'response': response_clean,
                    'sender': self.messages[i]['sender']
                })
        
        print(f"✅ Created {len(self.conversation_pairs)} conversation pairs")
        return self.conversation_pairs
    
    def generate_statistics(self):
        """Generate dataset statistics"""
        print("📊 Generating statistics...")
        
        total_messages = len(self.messages)
        senders = [msg['sender'] for msg in self.messages]
        sender_counts = Counter(senders)
        
        # Collect all words
        all_words = []
        for msg in self.messages:
            words = self.clean_text(msg['message']).split()
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        
        # Manglish word detection (approximate)
        manglish_keywords = [
            'entha', 'enthada', 'enthanu', 'eppo', 'evideyanu', 'evide',
            'alla', 'aayi', 'aakunna', 'aakanm', 'ano', 'ayit',
            'cheyyunnu', 'cheythu', 'cheyyan', 'kazhicho', 'kazhinju',
            'nallatha', 'nallathu', 'ooo', 'mm', 'aa', 'haa', 'illa',
            'ithokke', 'ath', 'ethu', 'eda', 'mone', 'da', 'machane',
            'bro', 'thanne', 'aane', 'undu', 'ilya', 'ariyla', 'pattum',
            'patilla', 'ini', 'pinne', 'sheri', 'seri', 'ketto', 'aarum'
        ]
        
        manglish_count = sum(1 for word in all_words if word in manglish_keywords)
        
        self.stats = {
            'total_messages': total_messages,
            'total_conversation_pairs': len(self.conversation_pairs),
            'unique_senders': len(sender_counts),
            'sender_distribution': dict(sender_counts.most_common()),
            'total_words': len(all_words),
            'unique_words': len(word_counts),
            'top_20_words': dict(word_counts.most_common(20)),
            'estimated_manglish_words': manglish_count,
            'manglish_percentage': round((manglish_count / len(all_words)) * 100, 2) if all_words else 0
        }
        
        return self.stats
    
    def save_processed_data(self, output_dir='data/processed'):
        """Save preprocessed data to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"💾 Saving processed data to {output_dir}/...")
        
        # Save conversation pairs as JSON
        pairs_file = os.path.join(output_dir, 'conversation_pairs.json')
        with open(pairs_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_pairs, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved conversation pairs to {pairs_file}")
        
        # Save as CSV for easy viewing
        csv_file = os.path.join(output_dir, 'conversation_pairs.csv')
        df = pd.DataFrame(self.conversation_pairs)
        df['context'] = df['context'].apply(lambda x: ' | '.join(x))
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"  ✓ Saved CSV to {csv_file}")
        
        # Save statistics
        stats_file = os.path.join(output_dir, 'dataset_statistics.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved statistics to {stats_file}")
        
        # Save cleaned messages
        messages_file = os.path.join(output_dir, 'cleaned_messages.json')
        with open(messages_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved cleaned messages to {messages_file}")
        
        print("✅ All data saved successfully!")
        
    def print_statistics(self):
        """Print dataset statistics in a readable format"""
        print("\n" + "="*60)
        print("📈 DATASET STATISTICS")
        print("="*60)
        print(f"Total Messages: {self.stats['total_messages']}")
        print(f"Total Conversation Pairs: {self.stats['total_conversation_pairs']}")
        print(f"Unique Senders: {self.stats['unique_senders']}")
        print(f"Total Words: {self.stats['total_words']}")
        print(f"Unique Words: {self.stats['unique_words']}")
        print(f"Estimated Manglish Words: {self.stats['estimated_manglish_words']}")
        print(f"Manglish Percentage: {self.stats['manglish_percentage']}%")
        
        print("\n📊 Sender Distribution:")
        for sender, count in list(self.stats['sender_distribution'].items())[:5]:
            print(f"  {sender}: {count} messages")
        
        print("\n🔤 Top 20 Most Common Words:")
        for word, count in list(self.stats['top_20_words'].items())[:20]:
            print(f"  {word}: {count}")
        
        print("="*60 + "\n")
    
    def show_sample_pairs(self, n=5):
        """Display sample conversation pairs"""
        print(f"\n💬 Sample Conversation Pairs (showing {n}):")
        print("="*60)
        for i, pair in enumerate(self.conversation_pairs[:n], 1):
            print(f"\nPair {i}:")
            print(f"  Context: {' | '.join(pair['context'])}")
            print(f"  Response: {pair['response']}")
            print(f"  Sender: {pair['sender']}")
        print("="*60 + "\n")


def main():
    """Main preprocessing pipeline"""
    print("\n🚀 WhatsApp Chat Preprocessor for Manglish Chatbot")
    print("="*60 + "\n")
    
    # Initialize preprocessor
    input_file = 'chats/WhatsApp Chat.txt'
    preprocessor = WhatsAppPreprocessor(input_file)
    
    # Step 1: Parse chat
    preprocessor.parse_whatsapp_chat()
    
    # Step 2: Create conversation pairs
    preprocessor.create_conversation_pairs(context_window=1)
    
    # Step 3: Generate statistics
    preprocessor.generate_statistics()
    
    # Step 4: Display statistics
    preprocessor.print_statistics()
    
    # Step 5: Show samples
    preprocessor.show_sample_pairs(n=10)
    
    # Step 6: Save processed data
    preprocessor.save_processed_data()
    
    print("\n✨ Preprocessing complete! Ready for chatbot training.\n")


if __name__ == "__main__":
    main()
