import re
from difflib import SequenceMatcher

# Normalize an address by removing specific keywords and non-alphanumeric characters
def normalize_address(address):
    address = re.sub(r'\b(Marg|Lane|Township)\b', '', address, flags=re.IGNORECASE)
    address = re.sub(r'\W+', ' ', address)
    return address.strip().lower()

# Check if two names match exactly (case-insensitive)
def exact_letter_match(name1, name2):
    return name1.strip().lower() == name2.strip().lower()

# Check if abbreviated names match, e.g., "John D" vs "John Doe"
def abbreviated_name_match(name1, name2):
    parts1, parts2 = name1.split(), name2.split()
    if len(parts1) == 2 and len(parts2) == 2:
        return parts1[0][0].lower() == parts2[0][0].lower() and parts1[1].lower() == parts2[1].lower()
    return False

# Ignore middle names while matching
def ignore_middle_names(name1, name2):
    parts1, parts2 = name1.split(), name2.split()
    if len(parts1) == 2 and len(parts2) == 3:
        return parts1[0].lower() == parts2[0].lower() and parts1[1].lower() == parts2[2].lower()
    if len(parts1) == 3 and len(parts2) == 2:
        return parts1[0].lower() == parts2[0].lower() and parts1[2].lower() == parts2[1].lower()
    return False

# Check if any part of one name matches with any part of another name
def match_any_part(name1, name2):
    parts1, parts2 = name1.lower().split(), name2.lower().split()
    return any(part in parts2 for part in parts1) or any(part in parts1 for part in parts2)

# Check if the sets of name components match, regardless of order
def circular_match(name1, name2):
    return set(name1.lower().split()) == set(name2.lower().split())

# Check single-letter abbreviation matches, e.g., "J Smith" vs "John Smith"
def single_letter_abbreviation(name1, name2):
    parts1, parts2 = name1.split(), name2.split()
    if len(parts1) == 2 and len(parts2) == 2:
        return parts1[0][0].lower() == parts2[0][0].lower() and parts1[1].lower() == parts2[1].lower()
    return False

# Match names based on multiple rules
def name_match(input_name, extracted_name):
    return (
        exact_letter_match(input_name, extracted_name) or
        abbreviated_name_match(input_name, extracted_name) or
        ignore_middle_names(input_name, extracted_name) or
        match_any_part(input_name, extracted_name) or
        circular_match(input_name, extracted_name) or
        single_letter_abbreviation(input_name, extracted_name)
    )

# Calculate similarity ratio between two strings
def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Match addresses based on normalization and similarity scores
def address_match(input_address, extracted_address, cutoff=70):
    input_address = normalize_address(input_address)
    extracted_address = normalize_address(extracted_address)

    input_fields, extracted_fields = input_address.split(), extracted_address.split()

    match_score = sum(
        max(similarity_ratio(field, efield) for efield in extracted_fields) * 100
        for field in input_fields
    )
    total_weight = len(input_fields) * 100

    final_score = (match_score / total_weight) if total_weight else 0

    pincode_match = (
        re.search(r'\d+', input_address) and
        re.search(r'\d+', extracted_address) and
        re.search(r'\d+', input_address).group() == re.search(r'\d+', extracted_address).group()
    )

    return pincode_match and final_score >= cutoff

# Check if UIDs match exactly
def uid_match(input_uid, extracted_uid):
    return input_uid.strip() == extracted_uid.strip()

# Evaluate the overall match based on name, address, and UID

def overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid):
    return (
        name_match(input_name, extracted_name) and
        address_match(input_address, extracted_address) and
        uid_match(input_uid, extracted_uid)
    )

# Example test cases to validate the functions
def run_tests():
    test_cases = [
        (
            "Rahul Dwivedi", "Rahul D",
            "B-404,4th floor,kphb,kphb colony entrance,Tower,hyderabad,Telangana,500001",
            "kphb colony entrance,Tower,hyderabad,Telangana,500001",
            "9860 03559198", "9860 0355 9198"
        ),
        (
            "Pushpam Kumar", "Kumar",
            "ward-10,1st,Rampur Dilawar,Vaishali,Near Hospital,Patna,Bihar-844124",
            "Vaishali,Bihar-844124",
            "9103 5715 3824", "9103 5715 3824"
        ),
        (
            "Adhithya", "Aditya",
            "Bilai,Durg,Chattisgarh,490006",
            "Bilai,Durg",
            "8028 5266 0990", "8028 5266 0990"
        )
    ]

    for input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid in test_cases:
        print(f"Testing: {input_name} vs {extracted_name}, {input_address} vs {extracted_address}, {input_uid} vs {extracted_uid}")
        print(f"Name Match: {name_match(input_name, extracted_name)}")
        print(f"Address Match: {address_match(input_address, extracted_address)}")
        print(f"UID Match: {uid_match(input_uid, extracted_uid)}")
        print(f"Overall Match: {overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid)}")

# Run the tests
run_tests()
