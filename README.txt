file all.extracted.csv from BACH
run:

python extract.py "3D structures_source.sdf"
python extract.py "drug sequences.fasta"

python .\convertFASTAtoSDF.py