#!/usr/bin/python3

# IMPORT REQUIRED MODULES #####################################################
import sqlite3
import argparse
from pathlib import Path
import re


# PATH & FILE DEFINING ########################################################
path = Path(__file__).resolve().parent.parent
db_file = sorted(Path(path).glob('*/*.sqlite'))[0]
outdir = Path(path)/"rst"
outdir.mkdir(parents=True, exist_ok=True)


# ARGUMENT PARSER #############################################################
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
                    help='list of genes, one per line; with default input ' +
                         'format is gene symbol'
                    )
parser.add_argument(
                    '-I',
                    dest='identifier',
                    metavar='<input_format>',
                    help='use to specify alternate input format, where the ' +
                         'available choices are "entrez_id", "ensembl_id", ' +
                         '"uniprot_acc", or "swissprot_id"',
                    default='gene_symbol'
                    )
parser.add_argument(
                    '-s',
                    dest='search_term',
                    metavar='"term"',
                    help='Check for disease associations in the database ' +
                         'containing <search_term>, and output associated' +
                         ' genes to <search_term>_associations.tab'
                    )
args = parser.parse_args()


# OPEN DATABASE FOR INTERACTION ###############################################
con = sqlite3.connect(str(db_file))
cur = con.cursor()  # Initialize cursor object.


# SOFTWARE CODE ###############################################################
if args.get_associations:  # If argument [-a] is specified.
    # Prints all associated diseases found within the database.
    diseases = []
    disease_file = str(outdir) + '/diseases.txt'
    statement = 'SELECT associations FROM gene_disease_associations'
    for row in cur.execute(statement).fetchall():
        # Iterate over all items, split them on the predefined delimiter,
        # and populate the diseases list.
        diseases.extend(row[0].split('|'))
    diseases = sorted(set(diseases))  # Remove duplicates.
    with open(disease_file, 'w') as out_file:
        for disease in diseases:
            print(disease, sep='n', file=out_file)

if args.infile:  # If argument [-i <input_file>] is specified.
    association_file = str(outdir/Path(args.infile).stem) + '_associations.txt'
    hits = []
    misses = []
    format_index = {
                    "entrez_id":1, "gene_symbol":2, "ensembl_id":3,
                    "uniprot_acc":4, "swissprot_id":5
                    }
    genes = [tuple(line.rstrip().split()) for line in open(args.infile, 'r')]
    statement_1 = 'SELECT * FROM id_table WHERE {}=?'.format(args.identifier)
    statement_2 = 'SELECT associations ' \
                  + 'FROM gene_disease_associations ' \
                  + 'WHERE id=?'
    for gene in genes:
        cur.execute(statement_1, gene)
        hits.append(cur.fetchone())
        if hits[-1] == None:
            misses.append(str(gene).strip('()').strip("',") + ', ')
    if misses:
        print('No associations were found for {}.'.format(
              ''.join(misses).strip(", ")))
    with open(association_file, 'w') as out_file:
        for hit in hits:
            if hit != None:
                cur.execute(statement_2, tuple(hit[0].split()))
                print(hit[format_index[args.identifier]],
                      ''.join(cur.fetchone()).replace('|',
                              '\n' + hit[format_index[args.identifier]] + '\t'
                              ),
                      sep='\t',
                      file=out_file
                      )

if args.search_term:  # If argument [-s "term"] is specified.
    # Uses the specified "term" to perform a search of the
    # associated diseases, and outputs tab-delimited gene-match pairs
    # to the search_file.
    search_file = str(outdir) + '/' + args.search_term + '_search_hits.txt'
    statement = 'SELECT i.gene_symbol, g.associations ' \
                + 'FROM gene_disease_associations g ' \
                + 'INNER JOIN id_table i ' \
                + 'ON g.id=i.id ' \
                + 'WHERE g.associations LIKE ?'
    # The search is executed in two phases, where (i) the search term is
    # first used in a query to the database,
    cur.execute(statement, tuple(('%' + args.search_term + '%').split()))
    with open(search_file, 'w') as out_file:
        for hit in cur:
            gene = hit[0]
            # and (ii) then used to extract the full disease association
            # matching the initial hit.
            association_hit = re.findall(('.*(?i)' + args.search_term + '.*'),
                                         hit[1].replace('|', '\n')
                                         )
            for disease in association_hit:
                    print(gene, disease, sep='\t', file=out_file)

con.close()  # Close connection to database.
