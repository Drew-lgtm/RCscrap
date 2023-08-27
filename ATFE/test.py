import re

# Sample text from your description
sample_text = "Skládací selfie dron HC-628 dream fly - RC_64557 od 1 222 Kč - Heureka.cz"

# Define the regular expression pattern
pattern = r"od (.*?) Kč"

# Use re.search to find the match in the sample text
match = re.search(pattern, sample_text)

# Check if a match is found
if match:
    # Get the captured text
    captured_text = match.group(1)
    print("Captured text:", captured_text)
else:
    print("No match found.")
