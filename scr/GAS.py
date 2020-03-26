#!/usr/bin/python3

import sqlite3
import argparse
from pathlib import Path

################################################################################
path = str(Path.cwd()) + '/'
db_file = str(path + 'db/gda.sqlite')

id_table = [
            "id", "entrez_id", "gene_symbol", "string_id",
            "uniprot_acc", "swissprot_id"
            ]
gene_disease_associations = ["id", "associations"]
protein_sequences = ["id", "sequence"]
go_compartment = ["id", "go_ids"]
go_functions = ["id", "go_ids"]
go_process = ["id", "go_ids"]
################################################################################

prog_usage = '''
Write the description for the program here.
             '''
parser = argparse.ArgumentParser(description=prog_usage)
parser.add_argument(
                    '-v',
                    '--version',
                    action='version',
                    version='%(prog)s 1.0'
                    )
parser.add_argument(
                    '-a',
                    dest='get_associations',
                    action='store_true',
                    help='output all diseases in the database to diseases.txt'
                    )
parser.add_argument(
                    '-i',
                    dest='infile',
                    metavar='<input_file>',
                    help='''
list of genes, one per line; default input format is gene symbol
                         '''
                    )
parser.add_argument(
                    '-o',
                    dest='outdir',
                    metavar='<output_path>',
                    help='specify output directory path'
                    )
parser.add_argument(
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
    statement = 'SELECT DISTINCT diseaseName FROM main ORDER BY diseaseName'
    cur.execute(statement)
    with open(str(path + 'data/diseases.txt'), 'w') as out_file:
        for disease in cur:
            print(''.join(map(str, disease)), sep='n', file=out_file)

if args.infile:
    file = str(Path(args.infile).stem + '_associations.txt')
    with open(file, 'w') as out_file:
        hits = []
        genes = [tuple(
                    line.rstrip().split()) for line in open(args.infile, 'r')]
        statement_1 = 'SELECT * FROM id_table WHERE gene_symbol=?'
        statement_2 = '''
SELECT associations FROM gene_disease_associations WHERE id=?
                      '''
        for gene in genes:
            cur.execute(statement_1, gene)
            hits.append(cur.fetchone())
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

con.close()
