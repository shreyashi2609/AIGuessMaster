import random
from game_logic import GameLogic

class AIHints:
    """Provides AI-powered hints for the number guessing game"""
    
    def __init__(self):
        self.game_logic = GameLogic()
        self.hint_templates = {
            'first_guess': [
                "Try starting with a number in the middle range (40-60) to narrow down quickly!",
                "A good strategy is to start with 50 and then adjust based on the feedback.",
                "Consider using the binary search approach - start with 50!"
            ],
            'too_high': [
                "You're getting closer! Try a number in the lower half of your current range.",
                "The number is definitely lower. Consider guessing in the {suggested_range} range.",
                "Good narrowing down! The secret number is below {current_guess}."
            ],
            'too_low': [
                "You're on the right track! Try a number in the upper half of your current range.",
                "The number is higher than that. Try something in the {suggested_range} range.",
                "Getting warmer! The secret number is above {current_guess}."
            ],
            'multiple_guesses': [
                "Based on your previous guesses, try focusing on the {suggested_range} range.",
                "You've made {attempts} attempts. Consider using the information from your previous guesses more strategically.",
                "Looking at your guess history, the number is likely in the {suggested_range} area."
            ],
            'encouragement': [
                "You're doing great! Keep using the feedback to narrow down your search.",
                "Good thinking! Each guess gives you valuable information about the number's location.",
                "You're getting closer with each guess. Trust the process!"
            ]
        }
    
    def generate_hint(self, current_guess, secret_number, previous_guesses):
        """
        Generate an intelligent hint based on the current game state
        
        Args:
            current_guess (int): The player's current guess
            secret_number (int): The secret number
            previous_guesses (list): List of all previous guesses
            
        Returns:
            str: A helpful hint for the player
        """
        # Determine the type of hint to give
        if len(previous_guesses) == 1:
            return self._get_first_guess_hint()
        
        # Analyze the current guess
        if current_guess > secret_number:
            return self._get_too_high_hint(current_guess, previous_guesses, secret_number)
        else:
            return self._get_too_low_hint(current_guess, previous_guesses, secret_number)
    
    def _get_first_guess_hint(self):
        """Generate a hint for the first guess"""
        return random.choice(self.hint_templates['first_guess'])
    
    def _get_too_high_hint(self, current_guess, previous_guesses, secret_number):
        """Generate a hint when the guess is too high"""
        # Find the highest guess that was too low
        too_low_guesses = [g for g in previous_guesses if g < secret_number]
        lower_bound = max(too_low_guesses) if too_low_guesses else 1
        
        # Find the lowest guess that was too high
        too_high_guesses = [g for g in previous_guesses if g > secret_number]
        upper_bound = min(too_high_guesses) if too_high_guesses else current_guess
        
        suggested_range = f"{lower_bound + 1}-{upper_bound - 1}"
        
        hint_template = random.choice(self.hint_templates['too_high'])
        return hint_template.format(
            suggested_range=suggested_range,
            current_guess=current_guess
        )
    
    def _get_too_low_hint(self, current_guess, previous_guesses, secret_number):
        """Generate a hint when the guess is too low"""
        # Find the highest guess that was too low
        too_low_guesses = [g for g in previous_guesses if g < secret_number]
        lower_bound = max(too_low_guesses) if too_low_guesses else current_guess
        
        # Find the lowest guess that was too high
        too_high_guesses = [g for g in previous_guesses if g > secret_number]
        upper_bound = min(too_high_guesses) if too_high_guesses else 100
        
        suggested_range = f"{lower_bound + 1}-{upper_bound - 1}"
        
        hint_template = random.choice(self.hint_templates['too_low'])
        return hint_template.format(
            suggested_range=suggested_range,
            current_guess=current_guess
        )
    
    def get_strategy_hint(self, previous_guesses, secret_number):
        """
        Provide a strategic hint based on the player's guessing pattern
        
        Args:
            previous_guesses (list): List of previous guesses
            secret_number (int): The secret number
            
        Returns:
            str: Strategic advice
        """
        if len(previous_guesses) < 2:
            return "Try to use each guess to eliminate half of the remaining possibilities!"
        
        # Analyze the player's strategy
        stats = self.game_logic.get_guess_statistics(previous_guesses, secret_number)
        
        if stats['average_difference'] > 30:
            return "Your guesses are quite far from the target. Try to use the feedback more systematically!"
        elif stats['average_difference'] < 10:
            return "You're getting very close! Try to be more precise with your next guess."
        else:
            return "You're making good progress. Keep narrowing down the range!"
    
    def get_encouragement_hint(self, attempts):
        """
        Provide encouraging feedback based on number of attempts
        
        Args:
            attempts (int): Number of attempts made
            
        Returns:
            str: Encouraging message
        """
        if attempts <= 3:
            return "Great start! You're learning about the number's location."
        elif attempts <= 6:
            return "You're making good progress! Keep using the feedback wisely."
        elif attempts <= 10:
            return "You're getting closer! Don't give up now."
        else:
            return "Persistence pays off! You're narrowing it down."
    
    def get_binary_search_hint(self, previous_guesses, secret_number):
        """
        Suggest using binary search strategy
        
        Args:
            previous_guesses (list): List of previous guesses
            secret_number (int): The secret number
            
        Returns:
            str: Binary search advice
        """
        if len(previous_guesses) == 0:
            return "Try starting with 50! This is the middle of the range and will help you eliminate half the possibilities."
        
        # Find the current search range
        too_low_guesses = [g for g in previous_guesses if g < secret_number]
        too_high_guesses = [g for g in previous_guesses if g > secret_number]
        
        lower_bound = max(too_low_guesses) if too_low_guesses else 1
        upper_bound = min(too_high_guesses) if too_high_guesses else 100
        
        suggested_guess = (lower_bound + upper_bound) // 2
        
        return f"Try guessing {suggested_guess}! This is the middle of your current search range ({lower_bound}-{upper_bound})."
