# PDF Merge Tool

### Installation

Run the following to install dependencies required for running this tool.

```
$ sudo apt-get install unoconv	
$ pip install pypdf2
```

### How to Use

Place all the files to be merged inside the `ToMerge` Folder.

Now `cd` into the root of the directory and run the script `merge.py`.

```
$ python merge.py
```

- The script first converts all the non-PDF files to PDF format.
- All files, including PDFs are moved from `ToMerge` to `Consumed`.
- The converted PDFs are then merged into one and then deleted from inside the `ToMerge` folder.
- Resultant PDF can be found inside the `Output` folder with the filename as printed on the terminal.
