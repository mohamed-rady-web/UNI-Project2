import sys
import os

# Make sure api/ directory is in path so game.py and ai.py can be imported
sys.path.insert(0, os.path.dirname(__file__))

from app import app
