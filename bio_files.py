# bio_files.py
# (1) Make FASTA sequences one-line
# (2) Parse BLAST text results (top hit per query)
# All outputs are saved into the "filtered/" folder.

# Convert multiline FASTA to one-line FASTA
def convert_multiline_fasta_to_oneline(input_fasta, output_name):
    """Join all sequence lines into one line per record and save to filtered/<output_name>."""
    output_fasta = "filtered/" + output_name

    input_handle = open(input_fasta, "r", encoding="utf-8", errors="ignore")
    output_handle = open(output_fasta, "w", encoding="utf-8")

    header = ""
    sequence = ""

    for line in input_handle:
        if line.startswith(">"):
            # write previous record (if any)
            if header != "":
                output_handle.write(header)
                output_handle.write(sequence + "\n")
            header = line.rstrip("\n")
            sequence = ""
        else:
            sequence += line.strip()

    # write last record
    if header != "":
        output_handle.write(header + "\n")
        output_handle.write(sequence + "\n")

    input_handle.close()
    output_handle.close()
    print("FASTA file saved to:", output_fasta)


# BLAST: take the first match for each input sequence
def parse_blast_output(input_file, output_name):
    """
    For each input sequence (Query) in a BLAST text report:
      - find the line 'Sequences producing significant alignments:'
      - take the FIRST real hit line under it (Description column)
      - collect unique descriptions, sort them, and save to filtered/<output_name>
    """
    output_file = "filtered/" + output_name
    proteins = []
    take_next = False

    input_handle = open(input_file, "r", encoding="utf-8", errors="ignore")
    for line in input_handle:
        line_no_newline = line.rstrip("\n")

        # new Query block
        if line_no_newline.startswith("Query=") or line_no_newline.startswith("QUERY="):
            take_next = False
            continue

        # header of the hits table
        if "Sequences producing significant alignments:" in line_no_newline:
            take_next = True
            continue

        if take_next:
            cleaned = line_no_newline.strip()

            # end of table
            if cleaned == "":
                take_next = False
                continue

            # skip obvious non-hit lines
            if (cleaned.startswith("Description") or cleaned.startswith("Score") or
                cleaned.startswith("E value") or cleaned.startswith("Expect") or
                cleaned.startswith("Accession") or cleaned.startswith("Length=") or
                cleaned.startswith(">") or cleaned.startswith("Database:") or
                "Scientific name" in cleaned or "Taxid" in cleaned):
                continue

            # find the first place with TWO consecutive spaces (BLAST column gap)
            gap_pos = -1
            for idx in range(len(cleaned) - 1):
                if cleaned[idx] == " " and cleaned[idx + 1] == " ":
                    gap_pos = idx
                    break

            if gap_pos == -1:
                # no column gap -> likely not a real hit line
                continue

            description = cleaned[:gap_pos].rstrip()
            right_columns = cleaned[gap_pos:].strip()

            # require that the right part looks numeric-ish (scores/e-values usually have digits)
            if not any(ch.isdigit() for ch in right_columns):
                continue

            proteins.append(description)
            take_next = False  # only the first hit per query

    input_handle.close()

    unique_sorted = sorted(set(proteins), key=str.lower) # remove duplicates and sort case-insensitively
    output_handle = open(output_file, "w", encoding="utf-8") # open file for writing (overwrite), using UTF-8 encoding
    for description in unique_sorted:
        output_handle.write(description + "\n")
    output_handle.close()

    print("BLAST results saved to:", output_file)
    return len(unique_sorted)
