import re
from difflib import SequenceMatcher

# Function to normalize address
def normalize_address(address):
    address = re.sub(r'\b(Marg|Lane|Township)\b', '', address, flags=re.IGNORECASE)
    address = re.sub(r'\W+', ' ', address)
    return address.strip().lower()

# Function to check exact letter match
def exact_letter_match(name1, name2):
    return name1.lower() == name2.lower()

# Function to check abbreviated name match
def abbreviated_name_match(name1, name2):
    name1_parts = name1.split()
    name2_parts = name2.split()
    if len(name1_parts) == 2 and len(name2_parts) == 2:
        return (name1_parts[0][0].lower() == name2_parts[0][0].lower() and
                name1_parts[1].lower() == name2_parts[1].lower())
    return False

# Function to check ignoring middle names match
def ignore_middle_names(name1, name2):
    parts1 = name1.split()
    parts2 = name2.split()
    if len(parts1) == 2 and len(parts2) == 3:
        return parts1[0].lower() == parts2[0].lower() and parts1[1].lower() == parts2[2].lower()
    if len(parts1) == 3 and len(parts2) == 2:
        return parts1[0].lower() == parts2[0].lower() and parts1[2].lower() == parts2[1].lower()
    return False

# Function to check matching any part of the name
def match_any_part(name1, name2):
    parts1 = name1.lower().split()
    parts2 = name2.lower().split()
    return any(part in parts2 for part in parts1) or any(part in parts1 for part in parts2)

# Function to check circular match
def circular_match(name1, name2):
    return set(name1.lower().split()) == set(name2.lower().split())

# Function to check single letter abbreviation match
def single_letter_abbreviation(name1, name2):
    parts1 = name1.split()
    parts2 = name2.split()
    if len(parts1) == 2 and len(parts2) == 2:
        return (parts1[0][0].lower() == parts2[0][0].lower() and
                parts1[1].lower() == parts2[1].lower())
    return False

# Function to match names based on various rules
def name_match(input_name, extracted_name):
    match_score = 0
    if exact_letter_match(input_name, extracted_name):
        match_score += 20
    if abbreviated_name_match(input_name, extracted_name):
        match_score += 20
    if ignore_middle_names(input_name, extracted_name):
        match_score += 20
    if match_any_part(input_name, extracted_name):
        match_score += 20
    if circular_match(input_name, extracted_name):
        match_score += 20
    if single_letter_abbreviation(input_name, extracted_name):
        match_score += 20
    return min(match_score, 100)

# Function to calculate similarity ratio
def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Functions to match specific address components
def house_flat_match(input_address, extracted_address):
    # Extract house/flat number from addresses
    house_flat_input = re.search(r'\b\d+[a-zA-Z]?\b', input_address)
    house_flat_extracted = re.search(r'\b\d+[a-zA-Z]?\b', extracted_address)
    if house_flat_input and house_flat_extracted:
        return similarity_ratio(house_flat_input.group(), house_flat_extracted.group()) * 100
    return 0

def street_road_match(input_address, extracted_address):
    # Extract street/road name from addresses
    input_address = normalize_address(input_address)
    extracted_address = normalize_address(extracted_address)
    input_street = ' '.join([word for word in input_address.split() if not word.isdigit()])
    extracted_street = ' '.join([word for word in extracted_address.split() if not word.isdigit()])
    return similarity_ratio(input_street, extracted_street) * 100

def city_match(input_address, extracted_address):
    # Extract city from addresses
    city_input = re.search(r'\b[a-zA-Z]+\b', input_address, re.IGNORECASE)
    city_extracted = re.search(r'\b[a-zA-Z]+\b', extracted_address, re.IGNORECASE)
    if city_input and city_extracted:
        return similarity_ratio(city_input.group(), city_extracted.group()) * 100
    return 0

def floor_number_match(input_address, extracted_address):
    # Extract floor number from addresses
    floor_input = re.search(r'\b\d+[a-zA-Z]*\b', input_address)
    floor_extracted = re.search(r'\b\d+[a-zA-Z]*\b', extracted_address)
    if floor_input and floor_extracted:
        return similarity_ratio(floor_input.group(), floor_extracted.group()) * 100
    return 0

def pincode_match(input_address, extracted_address):
    # Extract pin code from addresses
    pincode_input = re.search(r'\b\d{6}\b', input_address)
    pincode_extracted = re.search(r'\b\d{6}\b', extracted_address)
    if pincode_input and pincode_extracted:
        return similarity_ratio(pincode_input.group(), pincode_extracted.group()) * 100
    return 0

def premise_building_match(input_address, extracted_address):
    # Extract premise/building from addresses
    premise_input = re.search(r'\b[a-zA-Z]+\b', input_address, re.IGNORECASE)
    premise_extracted = re.search(r'\b[a-zA-Z]+\b', extracted_address, re.IGNORECASE)
    if premise_input and premise_extracted:
        return similarity_ratio(premise_input.group(), premise_extracted.group()) * 100
    return 0

def landmark_match(input_address, extracted_address):
    # Extract landmark from addresses if any (e.g., near, beside)
    landmark_input = re.search(r'\bnear\b.*', input_address, re.IGNORECASE)
    landmark_extracted = re.search(r'\bnear\b.*', extracted_address, re.IGNORECASE)
    if landmark_input and landmark_extracted:
        return similarity_ratio(landmark_input.group(), landmark_extracted.group()) * 100
    return 0

def state_match(input_address, extracted_address):
    # Extract state from addresses
    state_input = re.search(r'\b[a-zA-Z]+\b', input_address, re.IGNORECASE)
    state_extracted = re.search(r'\b[a-zA-Z]+\b', extracted_address, re.IGNORECASE)
    if state_input and state_extracted:
        return similarity_ratio(state_input.group(), state_extracted.group()) * 100
    return 0

# Function to match addresses based on normalization and field-specific matching
def address_match(input_address, extracted_address, cutoff=70):
    house_flat_score = house_flat_match(input_address, extracted_address)
    street_road_score = street_road_match(input_address, extracted_address)
    city_score = city_match(input_address, extracted_address)
    floor_number_score = floor_number_match(input_address, extracted_address)
    pincode_score = pincode_match(input_address, extracted_address)
    premise_building_score = premise_building_match(input_address, extracted_address)
    landmark_score = landmark_match(input_address, extracted_address)
    state_score = state_match(input_address, extracted_address)
    
    # Weighted sum of the individual scores
    final_score = (
        house_flat_score * 0.15 + 
        street_road_score * 0.15 + 
        city_score * 0.10 + 
        floor_number_score * 0.10 + 
        pincode_score * 0.15 + 
        premise_building_score * 0.10 + 
        landmark_score * 0.10 + 
        state_score * 0.15
    )

    if final_score >= cutoff:
        return final_score
    return final_score

# Function to check exact match for UID
def uid_match(input_uid, extracted_uid):
    return 100 if input_uid == extracted_uid else 0

# Function to match names based on various rules
def name_match(input_name, extracted_name):
    match_score = 0
    if exact_letter_match(input_name, extracted_name):
        match_score += 20
    if abbreviated_name_match(input_name, extracted_name):
        match_score += 20
    if ignore_middle_names(input_name, extracted_name):
        match_score += 20
    if match_any_part(input_name, extracted_name):
        match_score += 20
    if circular_match(input_name, extracted_name):
        match_score += 20
    if single_letter_abbreviation(input_name, extracted_name):
        match_score += 20
    return min(match_score, 100)

# Function to evaluate overall match
def overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid):
    name_score = name_match(input_name, extracted_name)
    address_score = address_match(input_address, extracted_address)
    uid_score = uid_match(input_uid, extracted_uid)
    overall_score = (name_score * 0.4) + (address_score * 0.4) + (uid_score * 0.2)  # Weights: 40% Name, 40% Address, 20% UID
    return overall_score

# Example usage and test cases
test_cases = [
    ("Rahul Dwivedi", "Rahul D", "B-404,4th floor,kphb,kphb colony entrance,Tower,hyderabad,Telangana,500001", "kphb colony entrance,Tower,hyderabad,Telangana,500001", "9860 03559198", "9860 0355 9198"),
    ("Pushpam Kumar","Kumar", "ward-10,1st,Rampur Dilawar,Vaishali,Near Hospital,Patna,Bihar-844124", "Vaishali,Bihar-844124", "9103 5715 3824", "9103 5715 3824"),
    ("Adhithya","Aditya","Bilai,Durg,Chattisgarh,490006","Bilai,Durg","8028 5266 0990","8028 5266 0990")
]

for input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid in test_cases:
    print(f"Testing: {input_name} vs {extracted_name}, {input_address} vs {extracted_address}, {input_uid} vs {extracted_uid}")
    print(f"Name Match Score: {name_match(input_name, extracted_name)}")
    print(f"House/Flat Match Score: {house_flat_match(input_address, extracted_address)}")
    print(f"Street/Road Match Score: {street_road_match(input_address, extracted_address)}")
    print(f"City Match Score: {city_match(input_address, extracted_address)}")
    print(f"Floor Number Match Score: {floor_number_match(input_address, extracted_address)}")
    print(f"Pincode Match Score: {pincode_match(input_address, extracted_address)}")
    print(f"Premise/Building Match Score: {premise_building_match(input_address, extracted_address)}")
    print(f"Landmark Match Score: {landmark_match(input_address, extracted_address)}")
    print(f"State Match Score: {state_match(input_address, extracted_address)}")
    print(f"Final Address Match Score: {address_match(input_address, extracted_address)}")
    print(f"UID Match Score: {uid_match(input_uid, extracted_uid)}")
    print(f"Overall Match Score: {overall_match(input_name, extracted_name, input_address, extracted_address, input_uid, extracted_uid)}")

