"""
Manglish Chatbot - Main Engine
===============================
A chatbot that understands and responds in Manglish (Malayalam written in English letters).
Uses rule-based patterns, intent recognition, and optional ML-based similarity matching.

Author: Chatbot_reborn Project
Date: December 2025
"""

import json
import re
import random
from difflib import SequenceMatcher
from collections import defaultdict
import os


class ManglishChatbot:
    """Main Manglish Chatbot Engine"""
    
    def __init__(self, conversation_data_path=None, quiet=False):
        """Initialize the chatbot with optional training data"""
        self.conversation_pairs = []
        self.intent_patterns = self._load_intent_patterns()
        self.responses_db = defaultdict(list)
        self.context_history = []
        self.max_context = 3
        self.quiet = quiet  # Suppress debug prints when True
        
        if conversation_data_path and os.path.exists(conversation_data_path):
            self.load_conversation_data(conversation_data_path)
    
    def _load_intent_patterns(self):
        """Load predefined intent patterns for Manglish"""
        return {
            'greeting': {
                'patterns': [
                    r'\b(hi|hello|hlo|hoi|hey|helo|hai)\b',
                    r'\b(entha|enthu|enthada|enthado|enthanu)\b',
                    r'\b(sukham|sukhamano|sukhamalle)\b',
                    r'\b(evideyanu|evideya|evidaya)\b'
                ],
                'responses': [
                    "Hlo! Entha vishesham?",
                    "Hey! Sukhamano?",
                    "Hi there! Entha cheyyunne?",
                    "Namaskaram! Samsarikam?",
                    "Hoi! Enthokeya paripadi?"
                ]
            },
            'how_are_you': {
                'patterns': [
                    r'\b(sukham|sukhamano|engane|enganeya|enganeyund)\b',
                    r'\b(kollalo|kollam|kollayirikkunu)\b',
                    r'(how are you|whats up|wassup)'
                ],
                'responses': [
                    "Nalla sukham! Ningal?",
                    "Kollam! Enthoru kadha?",
                    "Rasam! Engane pokunnu?",
                    "Adipoli! Samsarikam?",
                    "Super! Entha kaaryam?"
                ]
            },
            'food': {
                'patterns': [
                    r'\b(food|kazhicho|kazhikanam|vishakkunnu|vishakkund|sadhya)\b',
                    r'\b(meals|breakfast|lunch|dinner|kanji|choru|parotta)\b',
                    r'\b(biriyani|shawarma|vada|dosa|idli|puttu)\b'
                ],
                'responses': [
                    "Vishakkano? Entha kazhikkan ulla?",
                    "Food kazhicho? Enthayirunnu?",
                    "Nalla food kazhikanam! Entha ishttam?",
                    "Biriyani kazhikanam ennu thonnunnu!",
                    "Pwoli food! Evidennu kittum?"
                ]
            },
            'study': {
                'patterns': [
                    r'\b(padikkan|padippan|exam|record|assignment|graph|notes)\b',
                    r'\b(class|college|school|teacher|sir|mam)\b',
                    r'\b(complete|kazhinju|kazhinjille|kazhinjoo)\b'
                ],
                'responses': [
                    "Padikkanam! Exam ethrayanu?",
                    "Assignment kazhinjoo?",
                    "Record work complete aayo?",
                    "Sheri! Notes send cheyyam?",
                    "Class attend cheythoo?"
                ]
            },
            'time': {
                'patterns': [
                    r'\b(time|samayam|eppo|eppozhanu|ethrayayi)\b',
                    r'\b(neram|minute|hour|day|week)\b'
                ],
                'responses': [
                    "Time check cheytho?",
                    "Eppo venam?",
                    "Samayam kuravanu!",
                    "Ethra time und?",
                    "Neram nokkam!"
                ]
            },
            'affirmation': {
                'patterns': [
                    r'\b(aa|aah|yes|ok|okay|okey|seri|sheri|correct|right)\b',
                    r'\b(mm|hmm|aha|athe|thanne)\b',
                    r'\b(undu|und|undo)\b'
                ],
                'responses': [
                    "Seri! Pinne?",
                    "Ok! Entha vere?",
                    "Sheri! Next?",
                    "Mm! Continue cheyyam?",
                    "Athe! Pinne enthu?"
                ]
            },
            'negation': {
                'patterns': [
                    r'\b(illa|illya|ilya|no|nope|nop|alla|allallo)\b',
                    r'\b(venda|vendallo|kazhiyilla|kazhiyilla|patilla|patillallo)\b'
                ],
                'responses': [
                    "Alla? Pinne enthu?",
                    "Illa? Eni entha plan?",
                    "Ok illa! Mattethanu?",
                    "Poda venda! Enthayalum?",
                    "Seri! Vere enthelum?"
                ]
            },
            'thanks': {
                'patterns': [
                    r'\b(thanks|thank you|thankyou|nanni|nandri)\b',
                    r'\b(thanks a lot|thanks da|thanks machane)\b'
                ],
                'responses': [
                    "Welcome!",
                    "Parayan pattatha karyam!",
                    "Mention not!",
                    "Kuzhapamilla!",
                    "Santhosham!"
                ]
            },
            'help': {
                'patterns': [
                    r'\b(help|sahayam|thara|tharamo|vendee|venam)\b',
                    r'\b(entha cheyyuka|entha cheyya|enthanu cheyyendath)\b'
                ],
                'responses': [
                    "Entha help venam? Paranju tharam!",
                    "Tharum! Entha venda?",
                    "Sahayikkam! Entha kaaryam?",
                    "Vendath parayan! Ready!",
                    "Enth help? Parayu!"
                ]
            },
            'confusion': {
                'patterns': [
                    r'\b(manasilaayilla|ariyilla|ariyla|enthu|confusion)\b',
                    r'\b(doubt|enthadaa|enthada|enthanu|confused)\b'
                ],
                'responses': [
                    "Ariyillayo? Explain cheyyam!",
                    "Confusion? Ini paranju tharum!",
                    "Manasilaavillennu? Ok clear aakkam!",
                    "Doubt undo? Parayu!",
                    "Ariyilla? Simple! Kelkku!"
                ]
            }
        }
    
    def load_conversation_data(self, filepath):
        """Load preprocessed conversation pairs"""
        if not self.quiet:
            print(f"Loading conversation data from {filepath}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            self.conversation_pairs = json.load(f)
        
        # Build response database
        for pair in self.conversation_pairs:
            context = ' '.join(pair['context']) if isinstance(pair['context'], list) else pair['context']
            response = pair['response']
            self.responses_db[context.lower()].append(response)
        
        if not self.quiet:
            print(f"✅ Loaded {len(self.conversation_pairs)} conversation pairs")
    
    def clean_input(self, text):
        """Clean and normalize user input"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\?\!]', '', text)
        
        return text
    
    def detect_intent(self, text):
        """Detect user intent from text"""
        text_clean = self.clean_input(text)
        
        detected_intents = []
        for intent, data in self.intent_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, text_clean, re.IGNORECASE):
                    detected_intents.append(intent)
                    break
        
        return detected_intents if detected_intents else ['general']
    
    def find_similar_context(self, text, threshold=0.6):
        """Find similar context from training data using string similarity"""
        text_clean = self.clean_input(text)
        best_match = None
        best_score = 0
        
        for context, responses in self.responses_db.items():
            score = SequenceMatcher(None, text_clean, context).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = responses
        
        return best_match, best_score
    
    def generate_response(self, user_input):
        """Generate response based on user input"""
        # Clean input
        text_clean = self.clean_input(user_input)
        
        # Add to context history
        self.context_history.append(text_clean)
        if len(self.context_history) > self.max_context:
            self.context_history.pop(0)
        
        # Detect intents
        intents = self.detect_intent(text_clean)
        
        # Try intent-based response
        for intent in intents:
            if intent in self.intent_patterns:
                responses = self.intent_patterns[intent]['responses']
                return random.choice(responses), intent
        
        # Try similarity-based matching with training data
        if self.responses_db:
            similar_responses, score = self.find_similar_context(text_clean)
            if similar_responses and score > 0.6:
                return random.choice(similar_responses), f'similarity_{score:.2f}'
        
        # Fallback responses
        fallback_responses = [
            "Mm... Manasilayilla! Vere reethiyil parayamo?",
            "Entha paranjath? Repeat cheyyo?",
            "Ariyilla! Explain cheyyamo?",
            "Confusion! Koode vivaram parayamo?",
            "Hmmm... Clear aayi parayan pattumo?",
            "Entha udeshichath? Parayu!",
            "Ini parayunnath kelkkatte!",
            "Manasilakkan pattunnilla! Vere reethiyil parayu!"
        ]
        
        return random.choice(fallback_responses), 'fallback'
    
    def chat(self):
        """Interactive chat loop"""
        print("\n" + "="*60)
        print("🤖 Manglish Chatbot - Interactive Mode")
        print("="*60)
        print("Type 'exit', 'quit', or 'bye' to end the conversation")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'poda', 'poyi', 'pinne parayam']:
                    print("Bot: Seri! Pinne samsarikkam! Bye! 👋\n")
                    break
                
                # Generate response
                response, intent = self.generate_response(user_input)
                print(f"Bot: {response}")
                print(f"     [Intent: {intent}]\n")
                
            except KeyboardInterrupt:
                print("\n\nBot: Seri! Pinne kanam! 👋\n")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue


def main():
    """Main entry point"""
    print("\n🚀 Initializing Manglish Chatbot...")
    
    # Check if processed data exists
    data_path = 'data/processed/conversation_pairs.json'
    if os.path.exists(data_path):
        chatbot = ManglishChatbot(conversation_data_path=data_path)
    else:
        print("⚠️  No training data found. Using rule-based responses only.")
        print("   Run preprocess_whatsapp.py first to generate training data.")
        chatbot = ManglishChatbot()
    
    # Start interactive chat
    chatbot.chat()


if __name__ == "__main__":
    main()
