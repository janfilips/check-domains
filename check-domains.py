import itertools
import whois
import subprocess
import re
import time

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

print("Checking domain availability (this will take a few minutes)...")
for domain in candidate_domains:
    print(f"Checking {domain}...", end="")
    available = is_available(domain)
    print(" Available!" if available else " Taken.")
    if available:
        available_domains.append(domain)
    time.sleep(1)  # Be gentle to WHOIS servers

print("\n✅ Available Domains:")
for d in available_domains:
    print(d)
