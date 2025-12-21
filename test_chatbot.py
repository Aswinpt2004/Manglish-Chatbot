"""
Test Script for Manglish Chatbot
================================
Quick test to verify chatbot functionality with sample inputs
"""

from manglish_chatbot import ManglishChatbot


def test_intents():
    """Test various intent detections"""
    print("🧪 Testing Manglish Chatbot Intents\n")
    print("="*60)
    
    chatbot = ManglishChatbot()
    
    test_cases = [
        # Greetings
        ("hi entha vishesham", "greeting"),
        ("hello sukhamano", "greeting"),
        ("hlo machane", "greeting"),
        
        # Food
        ("food kazhicho", "food"),
        ("vishakkund da", "food"),
        ("biriyani venam", "food"),
        
        # Study
        ("assignment complete aayo", "study"),
        ("exam eppozhanu", "study"),
        ("record kazhinjoo", "study"),
        
        # Affirmation
        ("aa sheri", "affirmation"),
        ("ok ok", "affirmation"),
        ("mm correct", "affirmation"),
        
        # Negation
        ("illa venda", "negation"),
        ("no alla", "negation"),
        ("patilla", "negation"),
        
        # Thanks
        ("thanks da", "thanks"),
        ("thank you machane", "thanks"),
        
        # Help
        ("help venam", "help"),
        ("sahayam thara", "help"),
        
        # Time
        ("ethra time und", "time"),
        ("eppo venam", "time"),
        
        # Mixed/Complex
        ("food kazhicho? vishakkund da", "food"),
        ("hi entha plan today", "greeting"),
    ]
    
    passed = 0
    failed = 0
    
    for input_text, expected_intent in test_cases:
        response, detected_intent = chatbot.generate_response(input_text)
        
        # Check if expected intent is in detected intent
        intent_match = expected_intent in detected_intent or detected_intent == expected_intent
        
        status = "✅" if intent_match else "⚠️"
        passed += 1 if intent_match else 0
        failed += 0 if intent_match else 1
        
        print(f"\n{status} Input: {input_text}")
        print(f"   Expected: {expected_intent}")
        print(f"   Detected: {detected_intent}")
        print(f"   Response: {response}")
    
    print("\n" + "="*60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print(f"   Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print("="*60 + "\n")


def test_conversation_flow():
    """Test multi-turn conversation"""
    print("\n🗣️ Testing Conversation Flow\n")
    print("="*60)
    
    chatbot = ManglishChatbot()
    
    conversation = [
        "hi entha vishesham",
        "sukhamanu",
        "food kazhicho",
        "illa vishakkund",
        "biriyani kazhikanam",
        "ok sheri",
        "thanks da"
    ]
    
    print("Multi-turn conversation test:\n")
    for i, user_input in enumerate(conversation, 1):
        response, intent = chatbot.generate_response(user_input)
        print(f"Turn {i}:")
        print(f"  You: {user_input}")
        print(f"  Bot: {response}")
        print(f"  [Intent: {intent}]\n")
    
    print("="*60 + "\n")


def test_similarity_matching():
    """Test similarity-based matching (requires training data)"""
    print("\n🔍 Testing Similarity Matching\n")
    print("="*60)
    
    import os
    data_path = 'data/processed/conversation_pairs.json'
    
    if os.path.exists(data_path):
        chatbot = ManglishChatbot(conversation_data_path=data_path)
        
        test_inputs = [
            "ennik ariylaa",
            "record complete ano",
            "alla aakanm",
            "kazhinjoo",
            "nallatha"
        ]
        
        print("Testing with actual WhatsApp conversation data:\n")
        for user_input in test_inputs:
            response, intent = chatbot.generate_response(user_input)
            print(f"Input: {user_input}")
            print(f"Response: {response}")
            print(f"Method: {intent}\n")
    else:
        print("⚠️  Training data not found. Run preprocess_whatsapp.py first.")
    
    print("="*60 + "\n")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🤖 MANGLISH CHATBOT - TEST SUITE")
    print("="*60 + "\n")
    
    # Test 1: Intent recognition
    test_intents()
    
    # Test 2: Conversation flow
    test_conversation_flow()
    
    # Test 3: Similarity matching
    test_similarity_matching()
    
    print("✅ All tests completed!\n")


if __name__ == "__main__":
    main()
