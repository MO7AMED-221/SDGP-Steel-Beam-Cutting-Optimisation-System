import csv
from itertools import groupby

def smallest_combination(X: int, l: int):
    """
    Find (a,b,c) with:
      - 6000a + 8000b + 13000c >= X
      - a>0 => 6000 >= l, b>0 => 8000 >= l, c>0 => 13000 >= l
    Minimise total length, then number of coins, then lexicographic order.
    Returns (a,b,c, remaining) or None if no solution.
    """
    # Which beam lengths are allowed?
    allow_6000 = (6000 >= l)
    allow_8000 = (8000 >= l)
    allow_13000 = (13000 >= l)

    if not (allow_6000 or allow_8000 or allow_13000):
        return None   # No beam type can be used

    # Largest allowed beam (for safety bound)
    if allow_13000:
        L_max = 13000
    elif allow_8000:
        L_max = 8000
    else:
        L_max = 6000

    # Start from the smallest multiple of 1000 that is >= X
    T = ((X + 999) // 1000) * 1000

    while True:
        t = T // 1000          # work in units of 1000 mm
        best_for_T = None
        best_coins = float('inf')

        # Maximum number of 13000 beams (if allowed)
        max_c = (t // 13) if allow_13000 else 0

        for c in range(max_c + 1):
            rem = t - 13 * c
            if rem < 0:
                break

            # Try to find (a,b) for this c
            candidate = None

            if not allow_8000 and not allow_6000:
                # only (0,0) is allowed
                if rem == 0:
                    candidate = (0, 0, c)

            elif not allow_8000:
                # b must be 0
                if rem % 6 == 0:
                    a = rem // 6
                    if a == 0 or allow_6000:   # a>0 requires 6000 allowed
                        candidate = (a, 0, c)

            elif not allow_6000:
                # a must be 0
                if rem % 8 == 0:
                    b = rem // 8
                    if b == 0 or allow_8000:   # b>0 requires 8000 allowed
                        candidate = (0, b, c)

            else:  # both 6000 and 8000 are allowed
                if rem % 2 == 0:   # necessary condition for divisibility by 6
                    # We need the largest b <= rem//8 such that (rem - 8b) % 6 == 0
                    b_max = rem // 8
                    # Condition: 2b ≡ rem (mod 6)  =>  b ≡ rem/2 (mod 3)
                    k = rem // 2
                    r = k % 3
                    b = b_max - ((b_max - r) % 3)
                    if b >= 0:
                        a = (rem - 8 * b) // 6
                        # a and b are automatically non‑negative
                        candidate = (a, b, c)

            if candidate is not None:
                a, b, _ = candidate
                coins = a + b + c
                if coins < best_coins or (coins == best_coins and candidate < best_for_T):
                    best_for_T = candidate
                    best_coins = coins

        if best_for_T is not None:
            a, b, c = best_for_T
            return a, b, c, T - X

        # No solution for this T – try the next multiple of 1000
        T += 1000
        # Safety bound: we must eventually reach a solution (e.g., using one L_max beam)
        if T > X + L_max + 10000:   # generous upper limit
            return None


def process_csv(filepath: str, output_path: str):
    rows = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['_length'] = int(row['Length'])
                row['_total'] = int(row['TotalLength'])
            except (ValueError, KeyError):
                continue
            rows.append(row)

    rows.sort(key=lambda r: r['_length'])

    with open(output_path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(['BatchID', 'Length', 'RowCount', 'X', 'a', 'b', 'c', 'Remaining'])

        batch_id = 1
        for length_val, group in groupby(rows, key=lambda r: r['_length']):
            group_list = list(group)
            l = length_val
            X = sum(r['_total'] for r in group_list)

            result = smallest_combination(X, l)
            if result is None:
                a, b, c, remaining = 'N/A', 'N/A', 'N/A', 'N/A'
            else:
                a, b, c, remaining = result

            writer.writerow([batch_id, l, len(group_list), X, a, b, c, remaining])
            batch_id += 1

    print(f"Done. {batch_id - 1} batches written to '{output_path}'.")


if __name__ == "__main__":
    CSV_PATH = "Beam_Repository_DATA.csv"
    OUTPUT_PATH = "beam_results.csv"
    process_csv(CSV_PATH, OUTPUT_PATH)