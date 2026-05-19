
Notes modified today:
```dataview
list FROM ""
WHERE file.mday = date(this.file.name)
SORT file.mtime asc
```