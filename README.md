# Oook

## Oook is your librarian.
* It remembers your books and other electronic documents
* It can verify their integrity.
* It can search your library.

# Under construction...

## Usage:
* oook[.py] command library-db [options]

## Commands:
* verify - for each file in your library-db, generate a hash and compare with the stored hash
* scan - scan for new files

## Structure of library-db
The library-db file (conventionally called XXX.oook.csv for convenience) is a vertical-bar-separated
file that contains configuration parameters and a list of all the files in your library. The format can
be easily imported into a spreadsheet program for viewing and editing.

The file contains a number of rows, each of which is a record in the database.

### Record types
The first column of each row indicates the record type:

* Cfg - indicates a configuration parameter. The second column is the parameter name and the third column is its value
* Hdr - this record gives the column names for the file entries
* Doc - a file entry: contains information about a document
* Ign - a file entry: contains information about a file that you want to verify, but otherwise ignore
* New - a file entry: contains information about a new file that you haven't indexed yet

### Configuration parameters

* Root - the root directory of the library
* Hash - the type of hash to use for verification (default: sha512)

### Columns for file records

The columns can be given in any order (provided the record type is the first).

* Ident - a short identifier that can be used in (for example) a bibliography
* File - the base name of the file
* Path - the path (relative to Root) of the file
* Title - the title of the document
* Edition - any information about the edition or revision
* Author - who wrote it
* Date - when published
* Publisher - who published it
* Hash - the hash sum of the file

For the moment, File, Path and Hash are compulsory. You can add extra columns if you like
