"""
Demo Script - Manglish Chatbot Quick Start
==========================================
This script demonstrates the full pipeline:
1. Preprocessing WhatsApp data
2. Analyzing intents
3. Running the chatbot

Run this to see the complete workflow!
"""

import os
import sys


def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    try:
        import pandas
        print("  ✓ pandas installed")
        return True
    except ImportError:
        print("  ✗ pandas not found")
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt\n")
        return False


def check_data_file():
    """Check if WhatsApp chat file exists"""
    data_file = 'chats/WhatsApp Chat.txt'
    if os.path.exists(data_file):
        print(f"✓ Found WhatsApp chat file: {data_file}")
        return True
    else:
        print(f"✗ WhatsApp chat file not found: {data_file}")
        print("\n📝 To export WhatsApp chat:")
        print("   1. Open WhatsApp chat")
        print("   2. Tap the three dots (⋮) → More → Export chat")
        print("   3. Choose 'Without media'")
        print("   4. Save as 'WhatsApp Chat.txt' in the 'chats/' folder\n")
        return False


def run_preprocessing():
    """Run the preprocessing script"""
    print("\n" + "="*60)
    print("STEP 1: PREPROCESSING WHATSAPP DATA")
    print("="*60 + "\n")
    
    try:
        from preprocess_whatsapp import main as preprocess_main
        preprocess_main()
        return True
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return False


def run_intent_analysis():
    """Run intent analysis"""
    print("\n" + "="*60)
    print("STEP 2: ANALYZING INTENTS")
    print("="*60 + "\n")
    
    # Check if preprocessed data exists
    if not os.path.exists('data/processed/conversation_pairs.json'):
        print("⚠️  Skipping intent analysis - no preprocessed data found")
        return False
    
    try:
        from intent_analyzer import main as analyzer_main
        analyzer_main()
        return True
    except Exception as e:
        print(f"❌ Error during intent analysis: {e}")
        return False


def run_chatbot():
    """Run the interactive chatbot"""
    print("\n" + "="*60)
    print("STEP 3: RUNNING CHATBOT")
    print("="*60 + "\n")
    
    try:
        from manglish_chatbot import main as chatbot_main
        chatbot_main()
        return True
    except Exception as e:
        print(f"❌ Error running chatbot: {e}")
        return False


def main():
    """Main demo execution"""
    print("\n" + "="*60)
    print("🚀 MANGLISH CHATBOT - COMPLETE DEMO")
    print("="*60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data file
    if not check_data_file():
        print("\n⚠️  Cannot proceed without WhatsApp chat data.")
        print("   You can still run the chatbot with built-in patterns only:")
        print("   python manglish_chatbot.py\n")
        
        response = input("Do you want to run chatbot with built-in patterns only? (y/n): ")
        if response.lower() == 'y':
            run_chatbot()
        sys.exit(0)
    
    # Run full pipeline
    print("\n📋 Pipeline:")
    print("   1. Preprocess WhatsApp data")
    print("   2. Analyze intents")
    print("   3. Run interactive chatbot\n")
    
    input("Press Enter to start...")
    
    # Step 1: Preprocess
    if not run_preprocessing():
        print("\n❌ Preprocessing failed. Cannot continue.")
        sys.exit(1)
    
    # Step 2: Analyze
    run_intent_analysis()
    
    # Step 3: Run chatbot
    print("\n" + "="*60)
    print("Ready to chat! Starting chatbot...")
    print("="*60)
    input("\nPress Enter to start chatting...")
    
    run_chatbot()
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    print("\n📚 What's next?")
    print("   - Review generated data in data/processed/")
    print("   - Check intent analysis in data/intents/")
    print("   - Customize intents in manglish_chatbot.py")
    print("   - Add more training data\n")


if __name__ == "__main__":
    main()
