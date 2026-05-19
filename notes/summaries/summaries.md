---
title: summaries
created: 2025-01-25T19:29:29.263Z
modified: 2025-01-25T20:53:43.061Z
---


### Notes in folder

```dataview
TABLE file.folder, dateformat(file.mtime, "yy/MM/dd HH:mm") AS "Modified Time"
WHERE contains(file.folder, this.file.folder)
SORT file.mtime DESC
```
