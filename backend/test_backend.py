import requests
import json

# Base URL for the Flask app
BASE_URL = 'http://localhost:5000'

def test_start_game():
    """Test the /start endpoint"""
    print("Testing /start endpoint...")
    response = requests.post(f'{BASE_URL}/start')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Game started successfully!")
        print(f"   Message: {data['message']}")
        print(f"   Secret number: {data['secret_number']}")
        print(f"   Attempts: {data['attempts']}")
        return data['secret_number']
    else:
        print(f"❌ Failed to start game: {response.status_code}")
        return None

def test_make_guess(secret_number, guess, get_hint=False):
    """Test the /guess endpoint"""
    print(f"\nTesting /guess endpoint with guess: {guess}")
    
    payload = {
        'guess': guess,
        'get_hint': get_hint
    }
    
    response = requests.post(f'{BASE_URL}/guess', json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Guess processed successfully!")
        print(f"   Result: {data['result']}")
        print(f"   Correct: {data['correct']}")
        print(f"   Attempts: {data['attempts']}")
        if 'ai_hint' in data:
            print(f"   AI Hint: {data['ai_hint']}")
        if data.get('game_over'):
            print(f"   🎉 {data['final_message']}")
        return data['correct']
    else:
        print(f"❌ Failed to make guess: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_game_status():
    """Test the /status endpoint"""
    print("\nTesting /status endpoint...")
    response = requests.get(f'{BASE_URL}/status')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status retrieved successfully!")
        print(f"   Game active: {data['game_active']}")
        if data['game_active']:
            print(f"   Attempts: {data['attempts']}")
            print(f"   Guesses: {data['guesses']}")
        else:
            print(f"   Message: {data['message']}")
    else:
        print(f"❌ Failed to get status: {response.status_code}")

def test_reset_game():
    """Test the /reset endpoint"""
    print("\nTesting /reset endpoint...")
    response = requests.post(f'{BASE_URL}/reset')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Game reset successfully!")
        print(f"   Message: {data['message']}")
    else:
        print(f"❌ Failed to reset game: {response.status_code}")

def run_full_game_test():
    """Run a complete game test"""
    print("🎮 Starting Number Guessing Game Test")
    print("=" * 50)
    
    # Start a new game
    secret_number = test_start_game()
    if not secret_number:
        return
    
    # Test game status
    test_game_status()
    
    # Make some test guesses
    test_guesses = [25, 75, 50, 60, 55, secret_number]
    
    for i, guess in enumerate(test_guesses):
        # Get AI hint on every other guess
        get_hint = (i % 2 == 1)
        
        correct = test_make_guess(secret_number, guess, get_hint)
        
        if correct:
            print(f"\n🎉 Game won in {i + 1} attempts!")
            break
    
    # Test final status
    test_game_status()
    
    # Reset the game
    test_reset_game()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == '__main__':
    try:
        run_full_game_test()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask server.")
        print("   Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}") 