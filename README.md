# gDADs

The central software of gDADs (Gene-Disease Association Database Search-tool) is written in Python script. It seeks to streamline the process of enrichment analysis of a set of genes awarded from a differential expression study.

## Getting Started

These instructions will get you a copy of the software, and associated files, on your local machine for testing purposes (see section **Running tests**).

**Disclaimer:** gDADs was developed on a Linux system (Ubuntu 18.04.4 LTS) and should preferably be run on a Linux distribution of similar architecture. It might work on macOS, but is not compatible with Windows (as of version 1.0).

### Prerequisites

*Regrettably, no Anaconda environment file can be supplied at the moment, due to local update issues.*

The command-line executable was written in Python version 3.6.9, and only uses standard modules in the current iteration (version 1.0).

It was intended for [GOATOOLS](https://github.com/tanghaibao/goatools) to be implemented in the software, but this fell outside the scope of the project. Instead, a rudimentary function was added to gDADs version 1.0, tested in subsection **Running tests**.

### Installation

Start by either cloning the repository using git (code below), or downloading it directly from this page.

```
git clone https://github.com/yogogoba/gdads.git
```

This should be enough to run gDADs by calling the script located in the sub-directory /scr/. If it needs to be turned into an executable, use:

```
chmod /path/to/scr/gDADs +x
```

To link to your user bin folder, and run it as a command-line command:

```
ln -s ~/path/to/scr/gDADs ~/bin
```

To make sure that it is working, run it as follows to get some further information (where the first example requires linking it to your ~/bin):

```
gDADs -h
```

or,

```
~/path/to/scr/gDADs -h
```

or,

```
python3 ~/path/to/scr/gDADs -h
```

## Running tests

Testing can be done by utilizing the files contained within /data/test_in/. These hold example IDs, and should be specified with [-i \<input file\>], potentially using [-I]. The latter is needed to specify ID format, unless it is of default type ("`gene_symbol`"). The attained output files can then be compared to the files found in /data/test_out/.

### Example 1

```
~/path/to/scr/gDADs -i ~/path/to/data/test_in/deg_entrez.txt -I entrez_id
```

### Example 2

```
~/path/to/scr/gDADs -i ~/path/to/data/test_in/deg_symbol.txt -g "go_process"
```

### Example 3

```
~/path/to/scr/gDADs -s "hear"
```

## Built Using

* The command-line interface SQLite software ([sqlite3 3.22.0](https://sqlite.org/cli.html)) was used to create the SQLite database.
 * Tables were created from edited versions of the below files.
  * [curated_gene_disease_associations.tsv](https://www.disgenet.org/downloads)
  * [human.entrez_2_string.2018.tsv](https://string-db.org/mapping_files/entrez/)
  * [human.GO_2_string.2018](https://string-db.org/mapping_files/geneontology/)
  * [human.name_2_string.tsv](https://string-db.org/mapping_files/STRING_display_names/)
  * [human.uniprot_2_string.2018.tsv](https://string-db.org/mapping_files/uniprot/)

The database source files were trimmed to limit the scope and size, and enable upload to GitHub. They were reduced by first limiting the *curated_gene_disease_associations.tsv* by only including genes which were associated with inflammation. This was then further trimmed by matching the leftover IDs with those of the other source files.

## Author(s)

* **Joel Ströbaek**

## License

See [LICENCE](https://github.com/yogogoba/gdads/blob/master/LICENSE) file for information.
