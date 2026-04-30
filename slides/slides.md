---
title: slides
created: 2025-01-25T20:44:34.540Z
modified: 2025-01-25T20:52:34.986Z
---


### Notes in folder

```dataview
TABLE file.folder, dateformat(file.mtime, "yy/MM/dd HH:mm") AS "Modified Time"
WHERE contains(file.folder, this.file.folder)
SORT file.mtime DESC
```
