# Write a program that converts a Roman numeral to an integer

def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    # Iterate through the string in reverse
    for char in reversed(s):
        value = roman_values[char]
        # If current value is less than previous, subtract it
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    return total


# Test cases
print(roman_to_int("III"))      # 3
print(roman_to_int("LVIII"))    # 58
print(roman_to_int("MCMXCIV"))  # 1994

