class GameLogic:
    """Handles the core game logic for the number guessing game"""
    
    def __init__(self):
        self.min_number = 1
        self.max_number = 100
    
    def check_guess(self, guess, secret_number):
        """
        Check if a guess is correct, too high, or too low
        
        Args:
            guess (int): The player's guess
            secret_number (int): The secret number to guess
            
        Returns:
            dict: Contains 'correct' (bool) and 'message' (str)
        """
        if guess == secret_number:
            return {
                'correct': True,
                'message': 'Correct! You found the number!'
            }
        elif guess < secret_number:
            return {
                'correct': False,
                'message': f'Too low! The number is higher than {guess}.'
            }
        else:
            return {
                'correct': False,
                'message': f'Too high! The number is lower than {guess}.'
            }
    
    def validate_guess(self, guess):
        """
        Validate that a guess is within the valid range
        
        Args:
            guess: The guess to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            guess_int = int(guess)
            if guess_int < self.min_number or guess_int > self.max_number:
                return False, f'Guess must be between {self.min_number} and {self.max_number}'
            return True, None
        except (ValueError, TypeError):
            return False, 'Guess must be a valid number'
    
    def calculate_difference(self, guess, secret_number):
        """
        Calculate the absolute difference between guess and secret number
        
        Args:
            guess (int): The player's guess
            secret_number (int): The secret number
            
        Returns:
            int: Absolute difference
        """
        return abs(guess - secret_number)
    
    def get_guess_statistics(self, guesses, secret_number):
        """
        Get statistics about the player's guesses
        
        Args:
            guesses (list): List of previous guesses
            secret_number (int): The secret number
            
        Returns:
            dict: Statistics about the guesses
        """
        if not guesses:
            return {
                'total_guesses': 0,
                'closest_guess': None,
                'furthest_guess': None,
                'average_difference': 0
            }
        
        differences = [self.calculate_difference(g, secret_number) for g in guesses]
        
        return {
            'total_guesses': len(guesses),
            'closest_guess': min(guesses, key=lambda x: self.calculate_difference(x, secret_number)),
            'furthest_guess': max(guesses, key=lambda x: self.calculate_difference(x, secret_number)),
            'average_difference': sum(differences) / len(differences)
        }
    
    def is_guess_reasonable(self, guess, previous_guesses, secret_number):
        """
        Check if a guess is reasonable based on previous feedback
        
        Args:
            guess (int): The current guess
            previous_guesses (list): List of previous guesses
            secret_number (int): The secret number
            
        Returns:
            bool: True if the guess is reasonable
        """
        if not previous_guesses:
            return True
        
        # Check if the guess is within the range suggested by previous guesses
        for prev_guess in previous_guesses:
            if prev_guess < secret_number and guess <= prev_guess:
                return False  # Should guess higher
            elif prev_guess > secret_number and guess >= prev_guess:
                return False  # Should guess lower
        
        return True
