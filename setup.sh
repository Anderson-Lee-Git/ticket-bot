#!/bin/bash

# Step 1: Check if Homebrew is installed, if not, install Homebrew
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Step 2: Install Python 3 using Homebrew
if ! command -v python3 &> /dev/null
then
    echo "Installing Python 3..."
    brew install python
else
    echo "Python 3 is already installed."
fi

# Step 3: Upgrade pip (optional but recommended)
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Step 4: Install Selenium using pip
echo "Installing Selenium..."
python3 -m pip install selenium

# Step 5: Install webdriver-manager (optional but recommended for managing browser drivers)
echo "Installing webdriver-manager..."
python3 -m pip install webdriver-manager

# Step 6: Check if Git is installed, if not, install Git
if ! command -v git &> /dev/null
then
    echo "Git not found. Installing Git..."
    brew install git
else
    echo "Git is already installed."
fi

# Confirm Installation
echo "Python version: $(python3 --version)"
echo "Selenium version: $(python3 -m pip show selenium | grep Version)"
echo "webdriver-manager version: $(python3 -m pip show webdriver-manager | grep Version)"
echo "Git version: $(git --version)"

echo "Setup complete!"
