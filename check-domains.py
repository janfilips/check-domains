import itertools
import whois
import subprocess
import re
import time
from datetime import datetime, timezone
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Prefixes and suffixes with branding value
prefixes = list(dict.fromkeys([
    "mail", "pulse", "inbox", "clear", "swift", "zap", "trust", "true", "clean",
    "fast", "pro", "safe", "quick", "smart", "spot", "net", "prime", "core", "boost",
    "mail", "inbox", "bounce", "verify", "check", "email", "clear", "pure", "swift", "zap", "trust", "true", "pulse", "sense", "zero", "hero", "guard", "shield", "radar", "probe", "scout", "clean", "spot", "scan"
]))
suffixes = list(dict.fromkeys([
    "pulse", "mail", "check", "verify", "guard", "scan", "wave", "hero", "zone",
    "hub", "flux", "deck", "base", "spot", "nexus", "beacon", "craft", "works", "dock",
    "bounce", "guard", "check", "verify", "pulse", "shield", "radar", "sense", "wave", "hero", "clear", "swift", "spot", "scan", "edge", "boost", "nexus", "hub"
]))

# Generate all combinations and filter for "mail" or "pulse"
all_domains = [f"{p}{s}.com" for p, s in itertools.product(prefixes, suffixes)]
filtered_domains = [d for d in all_domains if "mail" in d or "pulse" in d]
filtered_domains = list(dict.fromkeys(filtered_domains))  # Remove duplicates

# Limit to 300
candidate_domains = filtered_domains[:300]

def is_available(domain):
    try:
        # Use system whois command
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout + result.stderr
        # Debug print of the raw whois output
        print(f"DEBUG: whois output for {domain}: {output}")
        # Check common patterns indicating the domain is available
        if re.search(r"No match for", output, re.IGNORECASE) \
           or re.search(r"NOT FOUND", output, re.IGNORECASE) \
           or re.search(r"No entries found", output, re.IGNORECASE):
            return True
        else:
            return False
    except Exception as e:
        print(f"DEBUG: whois subprocess exception for {domain}: {e}")
        # On error, assume taken to avoid false positives
        return False

available_domains = []

print("Checking domain info (this will take a few minutes)...")
for domain in candidate_domains:
    print(f"{domain}:", end=" ")
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout + result.stderr
        # Determine availability
        if re.search(r"No match for", output, re.IGNORECASE) \
           or re.search(r"NOT FOUND", output, re.IGNORECASE) \
           or re.search(r"No entries found", output, re.IGNORECASE):
            print(f"{RED}Available{RESET}")
            available_domains.append(domain)
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
                if days_left < 30:
                    exp_disp = f"{YELLOW}{exp_disp}{RESET}"
            else:
                exp_disp = "Unknown"
            print(f"Created: {creation_disp}, Expires: {exp_disp}")
    except Exception as e:
        print(f"Error retrieving info for {domain}: {e}")
    time.sleep(1)

print("\n✅ Available Domains:")
for d in available_domains:
    print(d)
