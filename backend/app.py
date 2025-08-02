from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random
from game_logic import GameLogic
from ai_hints import AIHints

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

# Initialize game logic and AI hints
game_logic = GameLogic()
ai_hints = AIHints()

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new number guessing game"""
    try:
        # Generate a new secret number
        secret_number = random.randint(1, 100)
        
        # Store game state in session
        session['secret_number'] = secret_number
        session['attempts'] = 0
        session['game_active'] = True
        session['guesses'] = []
        
        print(f"Game started! Secret number: {secret_number}, Session ID: {session.sid if hasattr(session, 'sid') else 'No SID'}")
        
        return jsonify({
            'message': 'Game started! Guess a number between 1 and 100.',
            'secret_number': secret_number,  # Remove this in production
            'attempts': 0
        }), 200
        
    except Exception as e:
        print(f"Error starting game: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/guess', methods=['POST'])
def make_guess():
    """Make a guess in the number guessing game"""
    try:
        print(f"Guess request received. Session data: {dict(session)}")
        
        # Check if game is active
        if not session.get('game_active', False):
            print("No active game found in session")
            return jsonify({'error': 'No active game. Start a new game first.'}), 400
        
        # Get the guess from request
        data = request.get_json()
        if not data or 'guess' not in data:
            return jsonify({'error': 'Guess is required'}), 400
        
        guess = data['guess']
        
        # Validate guess
        try:
            guess = int(guess)
            if guess < 1 or guess > 100:
                return jsonify({'error': 'Guess must be between 1 and 100'}), 400
        except ValueError:
            return jsonify({'error': 'Guess must be a valid number'}), 400
        
        # Get game state
        secret_number = session['secret_number']
        attempts = session['attempts']
        guesses = session.get('guesses', [])
        
        # Increment attempts
        attempts += 1
        session['attempts'] = attempts
        guesses.append(guess)
        session['guesses'] = guesses
        
        # Check the guess
        result = game_logic.check_guess(guess, secret_number)
        
        # Generate AI hint if requested
        ai_hint = None
        if data.get('get_hint', False) and not result['correct']:
            ai_hint = ai_hints.generate_hint(guess, secret_number, guesses)
        
        response = {
            'guess': guess,
            'result': result['message'],
            'correct': result['correct'],
            'attempts': attempts,
            'guesses': guesses
        }
        
        if ai_hint:
            response['ai_hint'] = ai_hint
        
        # If game is won, mark as inactive
        if result['correct']:
            session['game_active'] = False
            response['game_over'] = True
            response['final_message'] = f'Congratulations! You found the number in {attempts} attempts!'
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def game_status():
    """Get current game status"""
    try:
        if not session.get('game_active', False):
            return jsonify({'game_active': False, 'message': 'No active game'}), 200
        
        return jsonify({
            'game_active': True,
            'attempts': session.get('attempts', 0),
            'guesses': session.get('guesses', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the current game"""
    try:
        session.clear()
        return jsonify({'message': 'Game reset successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify backend is working"""
    return jsonify({'message': 'Backend is working!', 'session_id': id(session)}), 200

if __name__ == '__main__':
    print("🚀 Backend server starting...")
    print("🔗 Backend will be available at: http://localhost:5000")
    print("🎮 Frontend should connect from: http://localhost:3000")
    app.run(debug=True, host='0.0.0.0', port=5000)
