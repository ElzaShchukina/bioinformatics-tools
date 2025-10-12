# main_new.py
# Runs FASTQ filtering and saves the result to the "filtered/" folder

from fastq_utils import filter_fastq

def main_new():
    # Input and output file names
    inp = "example_data/example_fastq.fastq"   # file to read
    out = "output.fastq"                       # file to save inside 'filtered/'

    # Run filtering with simple settings
    filter_fastq(
        inp, out,
        min_len=3,        # minimal read length
        min_qual=30       # minimal average quality
    )

if __name__ == "__main__":
    main_new()