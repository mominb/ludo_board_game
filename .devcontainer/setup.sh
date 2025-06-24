#!/bin/bash

# Devcontainer Setup Script
# This script runs after the container is created to set up the development environment

set -e  # Exit on any error

echo "🚀 Starting devcontainer setup..."

# Update and upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Set up SSH directory permissions (if SSH directory exists)
if [ -d /home/vscode/.ssh ]; then
    echo "🔐 Setting up SSH permissions..."
    chmod 700 /home/vscode/.ssh
    chmod 600 /home/vscode/.ssh/* 2>/dev/null || true
    echo "✅ SSH permissions configured"
else
    echo "ℹ️  No SSH directory found, skipping SSH setup"
fi

# Configure Git with fallback values
echo "🔧 Configuring Git..."
current_name=$(git config --global user.name 2>/dev/null || echo "")
current_email=$(git config --global user.email 2>/dev/null || echo "")

if [ -z "$current_name" ]; then
    git config --global user.name "Your Name"
    echo "⚠️  Git user.name set to default. Please update with: git config --global user.name 'Your Actual Name'"
else
    echo "✅ Git user.name already set: $current_name"
fi

if [ -z "$current_email" ]; then
    git config --global user.email "your.email@example.com"
    echo "⚠️  Git user.email set to default. Please update with: git config --global user.email 'your@email.com'"
else
    echo "✅ Git user.email already set: $current_email"
fi

# Create useful aliases
echo "🛠️  Setting up useful aliases..."
cat >> /home/vscode/.bashrc << 'EOF'

# Ludo Game Development Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias pytest-cov='python -m pytest --cov=ludo_board_game --cov-report=html --cov-report=term'
alias run-tests='python -m pytest ludo_board_game/ -v'
alias run-game='python ludo_board_game/main.py'
alias lint='flake8 ludo_board_game/ && pylint ludo_board_game/ && mypy ludo_board_game/'
alias format='black ludo_board_game/ && isort ludo_board_game/'

EOF

# Also add aliases to zsh if it's being used
if [ -f /home/vscode/.zshrc ]; then
    cat >> /home/vscode/.zshrc << 'EOF'

# Ludo Game Development Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias pytest-cov='python -m pytest --cov=ludo_board_game --cov-report=html --cov-report=term'
alias run-tests='python -m pytest ludo_board_game/ -v'
alias run-game='python ludo_board_game/main.py'
alias lint='flake8 ludo_board_game/ && pylint ludo_board_game/ && mypy ludo_board_game/'
alias format='black ludo_board_game/ && isort ludo_board_game/'

EOF
fi

echo "✅ Aliases added to shell configuration"

# Display Python and tool versions
echo "🔍 Installed versions:"
python --version
pip --version
echo "black: $(black --version)"
echo "flake8: $(flake8 --version)"

echo ""
echo "🎉 Devcontainer setup completed successfully!"
echo ""
echo "📝 Available aliases:"
echo "  - run-game:    Start the Ludo game"
echo "  - run-tests:   Run all tests"
echo "  - pytest-cov: Run tests with coverage report"
echo "  - lint:        Run all linters (flake8, pylint, mypy)"
echo "  - format:      Format code with black and isort"
echo ""
echo "🚀 Happy coding!" 