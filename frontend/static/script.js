// Game state
let gameState = {
    isActive: false,
    attempts: 0,
    guesses: [],
    secretNumber: null
};

// API configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM elements
const elements = {
    startBtn: document.getElementById('startBtn'),
    resetBtn: document.getElementById('resetBtn'),
    submitGuess: document.getElementById('submitGuess'),
    playAgainBtn: document.getElementById('playAgainBtn'),
    guessInput: document.getElementById('guessInput'),
    getHint: document.getElementById('getHint'),
    gameStatus: document.getElementById('gameStatus'),
    guessSection: document.getElementById('guessSection'),
    resultsSection: document.getElementById('resultsSection'),
    hintSection: document.getElementById('hintSection'),
    historySection: document.getElementById('historySection'),
    attemptsCounter: document.getElementById('attemptsCounter'),
    celebration: document.getElementById('celebration'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    confettiContainer: document.getElementById('confettiContainer'),
    resultIcon: document.getElementById('resultIcon'),
    resultMessage: document.getElementById('resultMessage'),
    resultDetails: document.getElementById('resultDetails'),
    hintText: document.getElementById('hintText'),
    historyList: document.getElementById('historyList'),
    attemptsCount: document.getElementById('attemptsCount'),
    celebrationMessage: document.getElementById('celebrationMessage')
};

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkGameStatus();
});

// Setup event listeners
function setupEventListeners() {
    elements.startBtn.addEventListener('click', startGame);
    elements.resetBtn.addEventListener('click', resetGame);
    elements.submitGuess.addEventListener('click', submitGuess);
    elements.playAgainBtn.addEventListener('click', startGame);
    elements.guessInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitGuess();
        }
    });
    
    // Add input validation
    elements.guessInput.addEventListener('input', validateInput);
}

// Input validation
function validateInput() {
    const value = parseInt(elements.guessInput.value);
    const isValid = value >= 1 && value <= 100;
    
    elements.submitGuess.disabled = !isValid || !elements.guessInput.value;
    
    if (elements.guessInput.value && !isValid) {
        elements.guessInput.style.borderColor = '#ef4444';
    } else {
        elements.guessInput.style.borderColor = '#fce7f3';
    }
}

// Show loading overlay
function showLoading() {
    elements.loadingOverlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

// Show error message
function showError(message) {
    updateGameStatus('❌ ' + message, 'error');
    hideLoading();
}

// Update game status
function updateGameStatus(message, type = 'info') {
    const statusIcon = elements.gameStatus.querySelector('.status-icon');
    const statusText = elements.gameStatus.querySelector('.status-text');
    
    statusIcon.textContent = type === 'error' ? '❌' : '🎮';
    statusText.textContent = message;
    
    if (type === 'error') {
        elements.gameStatus.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            elements.gameStatus.style.animation = '';
        }, 500);
    }
}

// Check current game status
async function checkGameStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.game_active) {
            gameState.isActive = true;
            gameState.attempts = data.attempts;
            gameState.guesses = data.guesses;
            updateUIForActiveGame();
        } else {
            updateUIForInactiveGame();
        }
    } catch (error) {
        console.error('Error checking game status:', error);
        updateUIForInactiveGame();
    }
}

// Start a new game
async function startGame() {
    showLoading();
    
    try {
        console.log('Starting game...');
        const response = await fetch(`${API_BASE_URL}/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok) {
            gameState.isActive = true;
            gameState.attempts = 0;
            gameState.guesses = [];
            gameState.secretNumber = data.secret_number; // For development only
            
            updateUIForActiveGame();
            updateGameStatus('Game started! Guess a number between 1 and 100.');
            
            // Focus on input
            setTimeout(() => {
                elements.guessInput.focus();
            }, 500);
        } else {
            showError(data.error || 'Failed to start game');
        }
    } catch (error) {
        console.error('Error starting game:', error);
        showError('Failed to connect to server');
    }
    
    hideLoading();
}

// Submit a guess
async function submitGuess() {
    const guess = parseInt(elements.guessInput.value);
    
    if (!guess || guess < 1 || guess > 100) {
        showError('Please enter a valid number between 1 and 100');
        return;
    }
    
    showLoading();
    
    try {
        console.log('Submitting guess:', guess);
        const response = await fetch(`${API_BASE_URL}/guess`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                guess: guess,
                get_hint: elements.getHint.checked
            })
        });
        
        console.log('Guess response status:', response.status);
        const data = await response.json();
        console.log('Guess response data:', data);
        
        if (response.ok) {
            handleGuessResult(data);
        } else {
            showError(data.error || 'Failed to submit guess');
        }
    } catch (error) {
        console.error('Error submitting guess:', error);
        showError('Failed to connect to server');
    }
    
    hideLoading();
}

// Handle guess result
function handleGuessResult(data) {
    gameState.attempts = data.attempts;
    gameState.guesses = data.guesses;
    
    // Update attempts counter
    elements.attemptsCount.textContent = data.attempts;
    
    // Update result display
    updateResultDisplay(data);
    
    // Update history
    updateHistoryDisplay(data.guesses);
    
    // Clear input
    elements.guessInput.value = '';
    elements.submitGuess.disabled = true;
    
    // Check if game is won
    if (data.correct) {
        gameState.isActive = false;
        setTimeout(() => {
            showCelebration(data.final_message);
        }, 1000);
    } else {
        // Show hint if available
        if (data.ai_hint) {
            showHint(data.ai_hint);
        }
        
        // Focus back on input
        setTimeout(() => {
            elements.guessInput.focus();
        }, 500);
    }
}

// Update result display
function updateResultDisplay(data) {
    let icon, message, details;
    
    if (data.correct) {
        icon = '🎉';
        message = 'Correct! You found the number!';
        details = `Congratulations! You found the number in ${data.attempts} attempts!`;
    } else if (data.result.includes('Too high')) {
        icon = '📉';
        message = data.result;
        details = 'Try a lower number next time!';
    } else {
        icon = '📈';
        message = data.result;
        details = 'Try a higher number next time!';
    }
    
    elements.resultIcon.textContent = icon;
    elements.resultMessage.textContent = message;
    elements.resultDetails.textContent = details;
    
    elements.resultsSection.style.display = 'block';
}

// Show hint
function showHint(hint) {
    elements.hintText.textContent = hint;
    elements.hintSection.style.display = 'block';
}

// Update history display
function updateHistoryDisplay(guesses) {
    elements.historyList.innerHTML = '';
    
    guesses.forEach((guess, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.textContent = `#${index + 1}: ${guess}`;
        elements.historyList.appendChild(historyItem);
    });
    
    elements.historySection.style.display = 'block';
}

// Show celebration
function showCelebration(message) {
    elements.celebrationMessage.textContent = message;
    elements.celebration.style.display = 'flex';
    
    // Trigger confetti
    createConfetti();
    
    // Hide celebration after 5 seconds
    setTimeout(() => {
        elements.celebration.style.display = 'none';
    }, 5000);
}

// Create confetti animation
function createConfetti() {
    const colors = ['#ec4899', '#fbbf24', '#10b981', '#3b82f6', '#8b5cf6'];
    const confettiCount = 150;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            
            elements.confettiContainer.appendChild(confetti);
            
            // Remove confetti after animation
            setTimeout(() => {
                confetti.remove();
            }, 5000);
        }, i * 20);
    }
}

// Reset game
async function resetGame() {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/reset`, {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            gameState.isActive = false;
            gameState.attempts = 0;
            gameState.guesses = [];
            gameState.secretNumber = null;
            
            updateUIForInactiveGame();
            updateGameStatus('Game reset successfully!');
        } else {
            showError('Failed to reset game');
        }
    } catch (error) {
        console.error('Error resetting game:', error);
        showError('Failed to connect to server');
    }
    
    hideLoading();
}

// Update UI for active game
function updateUIForActiveGame() {
    elements.startBtn.style.display = 'none';
    elements.resetBtn.style.display = 'inline-flex';
    elements.guessSection.style.display = 'block';
    elements.attemptsCounter.style.display = 'block';
    elements.attemptsCount.textContent = gameState.attempts;
    
    if (gameState.guesses.length > 0) {
        elements.resultsSection.style.display = 'block';
        elements.historySection.style.display = 'block';
        updateHistoryDisplay(gameState.guesses);
    }
}

// Update UI for inactive game
function updateUIForInactiveGame() {
    elements.startBtn.style.display = 'inline-flex';
    elements.resetBtn.style.display = 'none';
    elements.guessSection.style.display = 'none';
    elements.resultsSection.style.display = 'none';
    elements.hintSection.style.display = 'none';
    elements.historySection.style.display = 'none';
    elements.attemptsCounter.style.display = 'none';
    elements.celebration.style.display = 'none';
    
    // Clear input
    elements.guessInput.value = '';
    elements.submitGuess.disabled = true;
}

// Add shake animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// Add smooth scrolling for better UX
document.documentElement.style.scrollBehavior = 'smooth';

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && elements.celebration.style.display === 'flex') {
        elements.celebration.style.display = 'none';
    }
});

// Add touch support for mobile
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}

// Add performance optimization
let animationFrameId;
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize input validation
const debouncedValidateInput = debounce(validateInput, 100);
elements.guessInput.addEventListener('input', debouncedValidateInput);

// Add accessibility features
elements.guessInput.setAttribute('aria-label', 'Enter your guess between 1 and 100');
elements.submitGuess.setAttribute('aria-label', 'Submit your guess');
elements.startBtn.setAttribute('aria-label', 'Start a new number guessing game');

// Add focus management
function manageFocus() {
    if (gameState.isActive) {
        elements.guessInput.focus();
    } else {
        elements.startBtn.focus();
    }
}

// Update focus when game state changes
const originalUpdateUIForActiveGame = updateUIForActiveGame;
updateUIForActiveGame = function() {
    originalUpdateUIForActiveGame();
    setTimeout(manageFocus, 100);
};

const originalUpdateUIForInactiveGame = updateUIForInactiveGame;
updateUIForInactiveGame = function() {
    originalUpdateUIForInactiveGame();
    setTimeout(manageFocus, 100);
};
