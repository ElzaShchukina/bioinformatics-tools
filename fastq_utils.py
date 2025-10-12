# fastq_utils.py
# Reads a FASTQ file, filters reads, and saves results to the "filtered/" folder.

def average_quality(quality_line):
    """Calculate the average PHRED33 quality (ASCII: 'I'=40, '!'=0)."""
    total = 0
    for ch in quality_line:
        total += ord(ch) - 33
    return total / len(quality_line)


def gc_percent(sequence):
    """Calculate GC percentage (fraction of G/C in the sequence)."""
    if len(sequence) == 0:
        return 0
    gc_count = 0
    for ch in sequence:
        if ch in "GgCc":
            gc_count += 1
    return 100 * gc_count / len(sequence)


def is_nucleic_acid(sequence):
    """Check that the sequence is DNA or RNA (not mixed T and U)."""
    if "T" in sequence and "U" in sequence:
        return False
    for ch in sequence:
        if ch not in "ACGTUacgtu":
            return False
    return True


def read_fastq(path):
    """Read a FASTQ file line by line, yielding one read at a time."""
    fh = open(path, "r", encoding="utf-8")
    while True:
        header = fh.readline()
        if not header:
            break
        sequence = fh.readline().strip()
        plus_line = fh.readline()
        quality = fh.readline().strip()
        if not quality:
            break
        yield header[1:].strip(), sequence, quality
    fh.close()


def filter_fastq(
    input_file,
    output_name,
    min_len=0,
    max_len=10**9,
    min_gc=0,
    max_gc=100,
    min_qual=0,
):
    """Filter reads and save the result into the folder 'filtered/'."""
    output_file = "filtered/" + output_name

    out = open(output_file, "w", encoding="utf-8")
    written = 0

    for read_name, sequence, quality in read_fastq(input_file):
        # Skip if sequence and quality lengths don't match
        if len(sequence) != len(quality):
            continue

        # Skip if it's not DNA or RNA
        if not is_nucleic_acid(sequence):
            continue

        # Skip if too short or too long
        if len(sequence) < min_len or len(sequence) > max_len:
            continue

        # Skip if GC content is out of bounds
        gc_pct = gc_percent(sequence)
        if gc_pct < min_gc or gc_pct > max_gc:
            continue

        # Skip if quality is too low
        if average_quality(quality) < min_qual:
            continue

        # Passed all filters -> save to file
        out.write(f"@{read_name}\n{sequence}\n+\n{quality}\n")
        written += 1

    out.close()
    print("Done! Reads saved:", written)
    print("File written to:", output_file)
    return written
