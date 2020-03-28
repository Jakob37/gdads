#!/usr/bin/python3

import sqlite3
import argparse
from pathlib import Path
import re

################################################################################
path = str(Path(__file__).resolve().parent.parent) + '/'
db_file = str(sorted(Path(path).glob('*/*.sqlite'))[0])

# id_table = [
#             "id", "entrez_id", "gene_symbol", "string_id",
#             "uniprot_acc", "swissprot_id"
#             ]
# gene_disease_associations = ["id", "associations"]
# protein_sequences = ["id", "sequence"]
# go_compartment = ["id", "go_ids"]
# go_functions = ["id", "go_ids"]
# go_process = ["id", "go_ids"]
################################################################################

prog_usage = '''
Write the description for the program here.
             '''
parser = argparse.ArgumentParser(description=prog_usage)
parser.add_argument( # -v
                    '-v',
                    '--version',
                    action='version',
                    version='%(prog)s 1.0'
                    )
parser.add_argument( # -a
                    '-a',
                    dest='get_associations',
                    action='store_true',
                    help='output all diseases in the database to diseases.txt'
                    )
parser.add_argument( # -i
                    '-i',
                    dest='infile',
                    metavar='<input_file>',
                    help='''
list of genes, one per line; default input format is gene symbol
                         '''
                    )
parser.add_argument( # -o
                    '-o',
                    dest='outdir',
                    metavar='<output_path>',
                    help='specify output directory path; defaults to ./rst/',
                    default=path + 'rst/'
                    )
parser.add_argument( # -s
                    '-s',
                    dest='search_term',
                    metavar='"term"',
                    help='''
Check for disease associations in the database containing <search_term>,
and output associated genes to <search_term>_associations.tab
                         '''
                    )

args = parser.parse_args()

con = sqlite3.connect(db_file)
cur = con.cursor()

if args.get_associations:
    # Prints all associated diseases found within the database.
    diseases = []
    if Path(args.outdir).exists():
        pass
    else:
        Path(path + 'rst').mkdir()
    file = str(args.outdir + 'diseases.txt')
    statement = '''
SELECT associations
FROM gene_disease_associations
                '''
    for row in cur.execute(statement).fetchall():
        # Iterate over all items, split them on the predefined delimiter,
        # and populate the diseases list.
        diseases.extend(row[0].split('|'))
    diseases = sorted(set(diseases))  # Remove duplicates.
    with open(file, 'w') as out_file:
        for disease in diseases:
            print(disease, sep='n', file=out_file)

if args.infile:
    file = str(args.outdir + Path(args.infile).stem) + '_associations.txt'
    hits = []
    genes = [tuple(
                line.rstrip().split()) for line in open(args.infile, 'r')]
    statement_1 = 'SELECT * FROM id_table WHERE gene_symbol=?'
    statement_2 = '''
SELECT associations
FROM gene_disease_associations
WHERE id=?
                  '''
    for gene in genes:
        cur.execute(statement_1, gene)
        hits.append(cur.fetchone())
    with open(file, 'w') as out_file:
        for hit in hits:
            if hit != None:
                cur.execute(statement_2, tuple(hit[0].split()))
                print(hit[2],
                      ''.join(cur.fetchone()).replace('|',
                              '\n' + hit[2] + '\t'
                              ),
                      sep='\t',
                      file=out_file
                      )

if args.search_term:
    file = str(args.outdir + args.search_term + '_search_hits.txt')
    hits = {}
    statement = '''
SELECT i.gene_symbol, g.associations
FROM gene_disease_associations g
INNER JOIN id_table i
ON g.id=i.id
WHERE g.associations LIKE ?
                '''
    cur.execute(statement, tuple(('%' + args.search_term + '%').split()))
    with open(file, 'w') as out_file:
        for hit in cur:
            gene = hit[0]
            association_hit = re.findall(('.*(?i)' + args.search_term + '.*'),
                                         hit[1].replace('|', '\n')
                                         )
            for disease in association_hit:
                    print(gene, disease, sep='\t', file=out_file)

con.close()
