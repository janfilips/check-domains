import itertools
import whois
import time

# Prefixes and suffixes with branding value
prefixes = [
    "mail", "pulse", "inbox", "clear", "swift", "zap", "trust", "true", "clean",
    "fast", "pro", "safe", "quick", "smart", "spot", "net", "prime", "core", "boost",
    "mail", "inbox", "bounce", "verify", "check", "email", "clear", "pure", "swift", "zap", "trust", "true", "pulse", "sense", "zero", "hero", "guard", "shield", "radar", "probe", "scout", "clean", "spot", "scan"
]
suffixes = [
    "pulse", "mail", "check", "verify", "guard", "scan", "wave", "hero", "zone",
    "hub", "flux", "deck", "base", "spot", "nexus", "beacon", "craft", "works", "dock",
    "bounce", "guard", "check", "verify", "pulse", "shield", "radar", "sense", "wave", "hero", "clear", "swift", "spot", "scan", "edge", "boost", "nexus", "hub"
]

# Generate all combinations and filter for "mail" or "pulse"
all_domains = [f"{p}{s}.com" for p, s in itertools.product(prefixes, suffixes)]
filtered_domains = [d for d in all_domains if "mail" in d or "pulse" in d]
filtered_domains = list(dict.fromkeys(filtered_domains))  # Remove duplicates

# Limit to 300
candidate_domains = filtered_domains[:300]

# WHOIS check
def is_available(domain):
    try:
        whois.whois(domain)
        return False  # Taken
    except:
        return True   # Likely available

available_domains = []

print("Checking domain availability (this will take a few minutes)...")
for domain in candidate_domains:
    print(f"Checking {domain}...", end="")
    if is_available(domain):
        available_domains.append(domain)
        print(" Available!")
    else:
        print(" Taken.")
    time.sleep(1)  # Be gentle to WHOIS servers

print("\n✅ Available Domains:")
for d in available_domains:
    print(d)
