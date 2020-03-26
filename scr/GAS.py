#!/usr/bin/python3

import sqlite3
import argparse
import os.path

################################################################################
path = str('/'.join(
            os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1]) + '/'
                    )
db_file = str(path + 'db/gda.sqlite')

id_table = ["id", "entrez_id", "gene_symbol", "string_id", "uniprot_acc",
            "swissprot_id"
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
                    '--all_associations',
                    action='store_true',
                    help='Output all diseases in the database to diseases.txt'
                    )
parser.add_argument(
                    '-i',
                    dest='deg_list',
                    help='''
List of genes, one per line, where the default input format is gene symbol
                         '''
                    )
parser.add_argument(
                    '-s',
                    dest='search_term',
                    help='''
Check for disease associations in the database containing <search_term>,
and output associated genes to <search_term>_associations.tab
                         '''
                    )
# parser.add_argument(
#                     '-o',
#                     dest='outfile',
#                     help=''
#                     )

args = parser.parse_args()

con = sqlite3.connect(db_file)
cur = con.cursor()

if args.d:
    statement = 'SELECT DISTINCT diseaseName FROM main ORDER BY diseaseName'
    cur.execute(statement)
    with open(str(path + 'data/diseases.txt'), 'w') as out_file:
        for disease in cur:
            print(''.join(map(str, disease)), sep='n', file=out_file)

if args.deg_list:
    genes = [tuple(
                line.rstrip().split()) for line in open(args.deg_list, "r")]
    statement = 'SELECT * FROM id_table WHERE gene_symbol=?'
    for gene in genes:
        cur.execute(statement, gene)
        print(cur.fetchone())

con.close()
