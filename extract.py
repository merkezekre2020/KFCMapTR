import sys, re, json

html = sys.stdin.read()
idx = html.find('initialRestaurants')
start = html.find('[', idx)

depth = 0
escape_next = False
i = start
for i in range(start, min(start + 2000000, len(html))):
    c = html[i]
    if escape_next:
        escape_next = False
        continue
    if c == '\\':
        escape_next = True
        continue
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0: break

raw = html[start:i+1]

# The data is JSON-inside-JSON (Next.js RSC serialization)
# Outer level has: \" for quote, \\ for backslash
# Inner JSON has: \" for quote, \\ for backslash
# So the raw string has: \\\\" for \" and \\\\ for \

# Strategy: decode the outer level first, then parse inner JSON
# Replace \\\\ with \  (double backslash -> single backslash)
# Then replace \\" with \" (escaped quote -> literal backslash-quote)
# But we need to be careful about order

# Better approach: just decode \\ -> \ and \" -> " in the right order
# Since \\\\ comes before \\" in the string, we process \\\\ first

result = []
j = 0
while j < len(raw):
    if j + 3 < len(raw) and raw[j:j+4] == '\\\\\\\"':
        # \\\\" -> \"
        result.append('\\"')
        j += 4
    elif j + 1 < len(raw) and raw[j:j+2] == '\\\\':
        # \\ -> \
        result.append('\\')
        j += 2
    elif j + 1 < len(raw) and raw[j:j+2] == '\\"':
        # \" -> "
        result.append('"')
        j += 2
    elif j + 1 < len(raw) and raw[j:j+2] == '\\/':
        # \/ -> /
        result.append('/')
        j += 2
    elif j + 1 < len(raw) and raw[j:j+2] == '\\n':
        result.append('\n')
        j += 2
    elif j + 1 < len(raw) and raw[j:j+2] == '\\u' and j+5 < len(raw):
        result.append(raw[j:j+6])
        j += 6
    else:
        result.append(raw[j])
        j += 1

cleaned = ''.join(result)

try:
    data = json.loads(cleaned)
except json.JSONDecodeError as e:
    print(f'JSON parse failed at position {e.pos}: {e.msg}', file=sys.stderr)
    print(f'Context: {repr(cleaned[max(0,e.pos-20):e.pos+20])}', file=sys.stderr)
    sys.exit(1)

with open('data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Toplam: {len(data)} sube')
cities = {}
for r in data:
    c = r.get('city', '?')
    cities[c] = cities.get(c, 0) + 1
for c, n in sorted(cities.items(), key=lambda x: -x[1])[:10]:
    print(f'{c}: {n}')
