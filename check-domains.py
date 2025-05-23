import whois
import time
import random

def is_domain_available(domain):
    try:
        whois.whois(domain)
        return False  # Domain is taken
    except Exception:
        return True  # Domain is available

# Generate potential domain names
prefixes = ["mail", "inbox", "bounce", "verify", "check", "email", "clear", "pure", "swift", "zap", "trust", "true", "pulse", "sense", "zero", "hero", "guard", "shield", "radar", "probe", "scout", "clean", "spot", "scan"]
suffixes = ["bounce", "guard", "check", "verify", "pulse", "shield", "radar", "sense", "wave", "hero", "clear", "swift", "spot", "scan", "edge", "boost", "nexus", "hub"]

# Create unique combinations
domains = set()
while len(domains) < 200:
    domain = random.choice(prefixes) + random.choice(suffixes) + ".com"
    domains.add(domain)

available_domains = []

print("Checking availability of domains...")
for domain in domains:
    print(f"Checking {domain}...", end="")
    if is_domain_available(domain):
        available_domains.append(domain)
        print(" Available!")
    else:
        print(" Taken.")
    time.sleep(1)  # Sleep to prevent IP rate limiting

print("\nAvailable domains:")
for domain in available_domains:
    print(domain)
