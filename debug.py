import sys, re, json

html = sys.stdin.read()
idx = html.find('initialRestaurants')
print(f"Found at index: {idx}")

# The data format is: "initialRestaurants":[{...}]
# But in Next.js RSC, it's escaped: "initialRestaurants\":[{\"id\":...
# So we need to handle the escaping

# Find the actual JSON array - it starts after "initialRestaurants":
# Look for the pattern: \"initialRestaurants\":[
search_start = idx
bracket_pos = html.find('[', search_start)
print(f"Bracket at: {bracket_pos}")

# Print context around the bracket
context = html[bracket_pos:bracket_pos+100]
print(f"Context: {repr(context[:100])}")
