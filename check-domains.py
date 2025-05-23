import itertools
import whois
import subprocess
import re
import time
from datetime import datetime, timezone
import os

# File to record free or near-expiry domains
selected_file = open('selected_domains.txt', 'w')

def run_whois_output(domain, retries=3, delay=0.1):
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(
                ["whois", domain],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            print(f"DEBUG: whois timeout for {domain}, attempt {attempt}/{retries}")
            time.sleep(delay)
    print(f"DEBUG: whois failed after {retries} retries for {domain}")
    return None

RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Threshold in days for considering a domain "close to expiry"
NEAR_EXPIRY_DAYS = 60

# Prefixes and suffixes with branding value
prefixes = list(dict.fromkeys([
    "spam", "mail", "pulse", "inbox", "clear", "swift", "zap", "trust", "true", "clean",
    "fast", "pro", "safe", "quick", "smart", "spot", "net", "prime", "core", "boost",
    "mail", "inbox", "bounce", "verify", "check", "email", "clear", "pure", "swift", "zap", "trust", "true", "pulse", "sense", "zero", "hero", "guard", "shield", "radar", "probe", "scout", "clean", "spot", "scan"
]))
suffixes = list(dict.fromkeys([
    "pulse", "mail", "check", "verify", "guard", "scan", "wave", "hero", "zone",
    "hub", "flux", "deck", "base", "spot", "nexus", "beacon", "craft", "works", "dock",
    "bounce", "guard", "check", "verify", "pulse", "shield", "radar", "sense", "wave", "hero", "clear", "swift", "spot", "scan", "edge", "boost", "nexus", "hub"
]))

all_domains = [f"{p}{s}.com" for p, s in itertools.product(prefixes, suffixes)]
filtered_domains = all_domains

# Limit to 300
candidate_domains = filtered_domains[:300]

def is_available(domain):
    output = run_whois_output(domain)
    if output is None:
        # Treat as taken if we couldn't get a response
        return False
    # Debug print of the raw whois output
    print(f"DEBUG: whois output for {domain}: {output}")
    # Check common patterns indicating the domain is available
    if re.search(r"No match for", output, re.IGNORECASE) \
       or re.search(r"NOT FOUND", output, re.IGNORECASE) \
       or re.search(r"No entries found", output, re.IGNORECASE):
        return True
    else:
        return False

available_domains = []

print("Checking domain info (this will take a few minutes)...")
for domain in candidate_domains:
    print(f"{domain}:", end=" ")
    output = run_whois_output(domain)
    if output is None:
        print(f"Error retrieving info for {domain}: timeout after retries")
        time.sleep(1)
        continue
    # Determine availability
    if re.search(r"No match for", output, re.IGNORECASE) \
       or re.search(r"NOT FOUND", output, re.IGNORECASE) \
       or re.search(r"No entries found", output, re.IGNORECASE):
        print(f"{RED}Available{RESET}")
        available_domains.append(domain)
        selected_file.write(domain + "\n")
        selected_file.flush()
        os.fsync(selected_file.fileno())
    else:
        # Extract creation and expiration dates
        creation_match = re.search(r"Creation Date:\s*(\S+)", output)
        expiry_match = re.search(r"Registry Expiry Date:\s*(\S+)", output) \
            or re.search(r"Expiration Date:\s*(\S+)", output)
        creation_str = creation_match.group(1) if creation_match else None
        expiry_str = expiry_match.group(1) if expiry_match else None
        creation_date = None
        expiry_date = None
        if creation_str:
            try:
                creation_date = datetime.fromisoformat(creation_str.replace('Z', '+00:00'))
            except:
                pass
        if expiry_str:
            try:
                expiry_date = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            except:
                pass
        creation_disp = creation_date.date().isoformat() if creation_date else "Unknown"
        if expiry_date:
            days_left = (expiry_date - datetime.now(timezone.utc)).days
            exp_disp = expiry_date.date().isoformat()
            if days_left <= NEAR_EXPIRY_DAYS:
                exp_disp = f"{YELLOW}{exp_disp}{RESET}"
                selected_file.write(domain + "\n")
                selected_file.flush()
                os.fsync(selected_file.fileno())
        else:
            exp_disp = "Unknown"
        print(f"Created: {creation_disp}, Expires: {exp_disp}")
    time.sleep(1)

print("\n✅ Available Domains:")
for d in available_domains:
    print(d)

selected_file.close()
