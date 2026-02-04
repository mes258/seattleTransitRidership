import csv

allStopsPath = "../../data/stopData/kcm/allStops.txt"
stopsToMergePath = "../../data/stopData/kcm/stops.txt"

def read_csv_as_dicts(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return reader.fieldnames, rows


# Read both files
header1, rows1 = read_csv_as_dicts(allStopsPath)
header2, rows2 = read_csv_as_dicts(stopsToMergePath)

# Build unified header (file 1 first, then new cols from file 2)
output_header = list(header1)
for col in header2:
    if col not in output_header:
        output_header.append(col)

# Index rows by stop_id
merged = {}

# Helper to normalize rows to full header
def normalize_row(row, header):
    return {col: row.get(col, "") for col in header}

# Load file 1 first
for row in rows1:
    stop_id = row["stop_id"]
    merged[stop_id] = normalize_row(row, output_header)

# Load file 2 (overwrites duplicates, adds new)
for row in rows2:
    stop_id = row["stop_id"]
    merged[stop_id] = normalize_row(row, output_header)

# Write output
with open(allStopsPath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=output_header)
    writer.writeheader()
    writer.writerows(merged.values())

print(f"Merged {len(merged)} unique stops into {allStopsPath}")