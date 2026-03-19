import sys, re, json

html = sys.stdin.read()
idx = html.find('initialRestaurants')
start = html.find('[', idx)

depth = 0
i = start
for i in range(start, min(start + 2000000, len(html))):
    c = html[i]
    if c == '\\' and i+1 < len(html):
        i += 1
        continue
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0: break

raw = html[start:i+1]

# Show around position 520
print(repr(raw[515:535]))
