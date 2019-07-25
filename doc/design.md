# Design of Oook

## Problem

I have a collection of assorted docmuents. Some of them are created by me, some are downloaded
from websites or even scanned. Many of them are different versions of the same document.

My documents are used by a large team of people who need to be able to add new documents, and new versions
of existing documents and - in some cases - remove documents.

All of the documents are binary files (PDF files, images, spreadsheets  etc.) so managing them using
git or some other source code control system is a nightmare. Apart from anything else, differences between
versions of "the same" document are difficult or impossible for source code control systems to manage,
so each new version is stored as a blob instead of a set of diffs. Yes I know git works like that for all
types of file.

If I try to use subversion I end up with a huge repository that seems to take an age to check out,
even though it might appear to contain only a few documents. Subversion is also not a distributed
system - I have to have a central server

With git, I get the distribution, but the checkout problem is far worse, because each clone contains
all versions of each document.

git LFS tries to help, but also takes a hit at checkout time.

git annex might have helped, but seems to be no longer maintained because of git LFS

Simply storing the files on a fileserver somewhere seems attractive, but I lose the
distributed copy feature. In addition, I have the problem that anyone who can put a new
document in the library can overwrite an old version or - even worse - delete documents.

But what if I used something like rsync to maintain multiple copies of my library?
I could keep a local copy of the library. In fact, there could be as many copies as necessary. But how to keep
track?


