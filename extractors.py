# extractors.py

import re

def extract_type_and_ticker(message_text):
    match = re.search(r'(LONG|SHORT):\s*(\w+)', message_text)
    return match.groups() if match else (None, None)

def extract_shock(message_text):
    match = re.search(r'SHOCK:\s*[$]?(?P<shock>\d+(\.\d+)?)', message_text)
    return float(match.group('shock')) if match else None

def extract_dist(message_text):
    match = re.search(r'DIST:\s*(?P<dist>\d+(\.\d+)?)%', message_text)
    return float(match.group('dist')) if match else None

# Test the functions on the provided messages

message1 = """
📗LONG: 1000PEPEUSDT📗

SHOCK: 0.007912
DIST: 0.11%
TARGET: $0.008405

SHOCKS
LG1: 0.007912
LG2: 0.0076522 3.3%
LG3: 0.0071592 6.4%

ALL TIME HIGH
PRICE: $0.0172768
DIST: 118.02%
"""

message2 = """
📕SHORT: LTCUSDT📕

SHOCK: $64.11
DIST: 0.14%
TARGET: $61.73

SHOCKS
ST1: 64.11
ST2: 64.97 1.3%
ST3: 67.35 3.7%

ALL TIME HIGH
PRICE: $413.94
DIST: 546.68%
"""

# Extract data from messages
def extract_data(message_text):
    type_and_ticker = extract_type_and_ticker(message_text)
    shock = extract_shock(message_text)
    dist = extract_dist(message_text)
    
    return {
        'type': type_and_ticker[0],
        'ticker': type_and_ticker[1],
        'shock': shock,
        'dist': dist
    }
