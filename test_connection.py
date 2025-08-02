import requests
import json

def test_backend_connection():
    """Test the backend connection and session handling"""
    base_url = 'http://localhost:5000'
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🧪 Testing Backend Connection")
    print("=" * 40)
    
    # Test 1: Check if backend is running
    try:
        response = session.get(f'{base_url}/test')
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5000")
        return False
    
    # Test 2: Start a game
    try:
        response = session.post(f'{base_url}/start')
        if response.status_code == 200:
            data = response.json()
            print("✅ Game started successfully")
            print(f"   Secret number: {data.get('secret_number')}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Failed to start game: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        return False
    
    # Test 3: Check game status
    try:
        response = session.get(f'{base_url}/status')
        if response.status_code == 200:
            data = response.json()
            print("✅ Game status retrieved")
            print(f"   Game active: {data.get('game_active')}")
            print(f"   Attempts: {data.get('attempts')}")
        else:
            print(f"❌ Failed to get status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return False
    
    # Test 4: Make a guess
    try:
        response = session.post(f'{base_url}/guess', 
                              json={'guess': 50, 'get_hint': True})
        if response.status_code == 200:
            data = response.json()
            print("✅ Guess submitted successfully")
            print(f"   Result: {data.get('result')}")
            print(f"   Correct: {data.get('correct')}")
            print(f"   Attempts: {data.get('attempts')}")
            if 'ai_hint' in data:
                print(f"   AI Hint: {data.get('ai_hint')}")
        else:
            print(f"❌ Failed to submit guess: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error submitting guess: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("✅ All tests passed! Backend is working correctly.")
    return True

if __name__ == '__main__':
    test_backend_connection() 