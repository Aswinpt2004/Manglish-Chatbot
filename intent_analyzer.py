"""
Intent Trainer and Analyzer for Manglish Chatbot
=================================================
This module provides tools to analyze training data, identify common intents,
and improve the chatbot's understanding of Manglish patterns.
"""

import json
import re
from collections import Counter, defaultdict
import os


class IntentAnalyzer:
    """Analyze conversation data to identify and extract intents"""
    
    def __init__(self, conversation_data_path):
        self.data_path = conversation_data_path
        self.conversation_pairs = []
        self.word_frequency = Counter()
        self.bigram_frequency = Counter()
        self.intent_clusters = defaultdict(list)
        
        self.load_data()
    
    def load_data(self):
        """Load conversation pairs"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.conversation_pairs = json.load(f)
        print(f"✅ Loaded {len(self.conversation_pairs)} conversation pairs")
    
    def analyze_word_frequency(self):
        """Analyze word frequency in conversations"""
        print("📊 Analyzing word frequency...")
        
        for pair in self.conversation_pairs:
            # Get all text
            if isinstance(pair['context'], list):
                text = ' '.join(pair['context']) + ' ' + pair['response']
            else:
                text = pair['context'] + ' ' + pair['response']
            
            # Tokenize
            words = text.lower().split()
            self.word_frequency.update(words)
            
            # Create bigrams
            bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
            self.bigram_frequency.update(bigrams)
        
        return self.word_frequency, self.bigram_frequency
    
    def extract_common_patterns(self, top_n=50):
        """Extract common Manglish patterns"""
        print(f"🔍 Extracting top {top_n} patterns...")
        
        # Common Manglish question words
        question_words = ['entha', 'enthada', 'enthanu', 'eppo', 'evide', 'evideyanu',
                         'engane', 'ethu', 'ethra', 'aaranu', 'aar', 'enthinu']
        
        # Common Manglish verbs
        verbs = ['cheyyunnu', 'cheythu', 'cheyyan', 'kazhicho', 'kazhinju',
                'undu', 'illa', 'aanu', 'aayi', 'ayit', 'venam', 'venda']
        
        patterns = {
            'top_words': dict(self.word_frequency.most_common(top_n)),
            'top_bigrams': dict(self.bigram_frequency.most_common(top_n)),
            'question_words_found': {w: self.word_frequency[w] for w in question_words if self.word_frequency[w] > 0},
            'verbs_found': {w: self.word_frequency[w] for w in verbs if self.word_frequency[w] > 0}
        }
        
        return patterns
    
    def cluster_by_keywords(self):
        """Cluster conversations by key Manglish keywords"""
        print("🎯 Clustering conversations by keywords...")
        
        keyword_categories = {
            'greeting': ['hi', 'hello', 'hlo', 'hey', 'hai', 'entha', 'sukham'],
            'food': ['food', 'kazhicho', 'kazhikanam', 'vishakkund', 'biriyani', 'choru', 'meals'],
            'study': ['padikkan', 'exam', 'record', 'assignment', 'class', 'college', 'notes', 'graph'],
            'time': ['time', 'samayam', 'eppo', 'neram', 'ethra'],
            'location': ['evide', 'evideyanu', 'evidaya', 'place'],
            'affirmation': ['aa', 'yes', 'ok', 'seri', 'sheri', 'mm', 'undu'],
            'negation': ['illa', 'illya', 'no', 'alla', 'venda', 'patilla'],
            'help': ['help', 'sahayam', 'thara', 'venam', 'vendee'],
            'thanks': ['thanks', 'thank', 'nanni', 'nandri']
        }
        
        for pair in self.conversation_pairs:
            if isinstance(pair['context'], list):
                text = ' '.join(pair['context']).lower()
            else:
                text = pair['context'].lower()
            
            response = pair['response'].lower()
            full_text = text + ' ' + response
            
            # Check which categories this conversation belongs to
            for category, keywords in keyword_categories.items():
                for keyword in keywords:
                    if keyword in full_text:
                        self.intent_clusters[category].append({
                            'context': pair['context'],
                            'response': pair['response']
                        })
                        break
        
        # Print cluster sizes
        print("\n📦 Intent Cluster Sizes:")
        for category, items in sorted(self.intent_clusters.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {category}: {len(items)} conversations")
        
        return self.intent_clusters
    
    def generate_intent_training_data(self, output_dir='data/intents'):
        """Generate structured intent training data"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n💾 Generating intent training data in {output_dir}/...")
        
        # Save each intent cluster
        for intent, conversations in self.intent_clusters.items():
            if len(conversations) > 0:
                filepath = os.path.join(output_dir, f'{intent}_examples.json')
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(conversations, f, ensure_ascii=False, indent=2)
                print(f"  ✓ Saved {len(conversations)} examples for '{intent}'")
        
        # Save word frequency data
        freq_file = os.path.join(output_dir, 'word_frequency.json')
        with open(freq_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.word_frequency.most_common(200)), f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved word frequency data")
        
        # Save bigram frequency
        bigram_file = os.path.join(output_dir, 'bigram_frequency.json')
        with open(bigram_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.bigram_frequency.most_common(100)), f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved bigram frequency data")
        
        print("✅ Intent training data generated!")
    
    def suggest_new_intents(self, min_frequency=5):
        """Suggest new intents based on unmatched common patterns"""
        print(f"\n💡 Suggesting new intents (min frequency: {min_frequency})...")
        
        # Get clustered words
        clustered_words = set()
        keyword_categories = {
            'greeting': ['hi', 'hello', 'hlo', 'hey', 'hai', 'entha', 'sukham'],
            'food': ['food', 'kazhicho', 'kazhikanam', 'vishakkund', 'biriyani', 'choru'],
            'study': ['padikkan', 'exam', 'record', 'assignment', 'class', 'college'],
            'time': ['time', 'samayam', 'eppo', 'neram'],
            'affirmation': ['aa', 'yes', 'ok', 'seri', 'mm'],
            'negation': ['illa', 'no', 'alla', 'venda']
        }
        
        for keywords in keyword_categories.values():
            clustered_words.update(keywords)
        
        # Find frequent words not in any cluster
        suggestions = []
        for word, count in self.word_frequency.most_common(100):
            if count >= min_frequency and word not in clustered_words and len(word) > 2:
                suggestions.append((word, count))
        
        if suggestions:
            print("\n🆕 Suggested words for new intents:")
            for word, count in suggestions[:20]:
                print(f"  {word}: {count} occurrences")
        
        return suggestions


def main():
    """Main analysis pipeline"""
    print("\n🔬 Intent Analyzer for Manglish Chatbot")
    print("="*60 + "\n")
    
    # Load data
    data_path = 'data/processed/conversation_pairs.json'
    if not os.path.exists(data_path):
        print("❌ Error: Processed data not found!")
        print("   Please run preprocess_whatsapp.py first.")
        return
    
    # Initialize analyzer
    analyzer = IntentAnalyzer(data_path)
    
    # Analyze word frequency
    word_freq, bigram_freq = analyzer.analyze_word_frequency()
    
    # Extract patterns
    patterns = analyzer.extract_common_patterns(top_n=30)
    
    print("\n📊 Top 30 Most Common Words:")
    for word, count in list(patterns['top_words'].items())[:30]:
        print(f"  {word}: {count}")
    
    print("\n📊 Top 20 Most Common Bigrams:")
    for bigram, count in list(patterns['top_bigrams'].items())[:20]:
        print(f"  '{bigram}': {count}")
    
    # Cluster conversations
    clusters = analyzer.cluster_by_keywords()
    
    # Show sample from each cluster
    print("\n📚 Sample Conversations by Intent:")
    for intent, conversations in list(clusters.items())[:3]:
        if conversations:
            print(f"\n{intent.upper()} (showing first example):")
            sample = conversations[0]
            if isinstance(sample['context'], list):
                print(f"  Context: {' | '.join(sample['context'])}")
            else:
                print(f"  Context: {sample['context']}")
            print(f"  Response: {sample['response']}")
    
    # Generate training data
    analyzer.generate_intent_training_data()
    
    # Suggest new intents
    suggestions = analyzer.suggest_new_intents(min_frequency=5)
    
    print("\n✅ Intent analysis complete!")


if __name__ == "__main__":
    main()
