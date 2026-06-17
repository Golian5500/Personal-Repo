import sys
import os

# Add the project directory to sys.path to import luhn_check
sys.path.append(os.path.dirname(__file__))
from app import luhn_check

def test_luhn():
    # Example valid Visa card number
    valid_card = "4111111111111111"
    invalid_card = "4111111111111112"
    
    print(f"Testing valid card: {valid_card}")
    result_valid = luhn_check(valid_card)
    print(f"Result: {result_valid}")
    
    print(f"Testing invalid card: {invalid_card}")
    result_invalid = luhn_check(invalid_card)
    print(f"Result: {result_invalid}")

    # Another valid Master Card example
    valid_master = "5500000000000004"
    print(f"Testing valid master card: {valid_master}")
    result_valid_master = luhn_check(valid_master)
    print(f"Result: {result_valid_master}")

if __name__ == "__main__":
    test_luhn()