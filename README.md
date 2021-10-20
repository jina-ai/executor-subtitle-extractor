# SubtitleExtractor
Subtile extractor helps extracting text from the `.vtt` files and using the heuristics to remove the duplicated text.        

## Usage
Suppose you have already downloaded a `.vtt` file:

```python

data_fn = $PATH_OF_YOUR_VTT_FILE
docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
f = Flow().add(uses='jinahub://SubtitleExtractor')
with f:
    f.post(inputs=docs)
```
Your input should be `.vtt` files, and for documents in docs, it will be divided into several chunks, each chunk contains their text and time information like follow:
```
{'id': '2b5d7ac6-3180-11ec-9f3a-acde48001122_0', 'mime_type': 'text/plain', 'tags': {'beg_in_seconds': 1.04, 'end_in_seconds': 4.789, 'vid': 'zvXkQkqd2I8.vtt'}, 'text': 'hi my name is han founder and ceo of jina ai', 'granularity': 1, 'parent_id': '2b5d7ac6-3180-11ec-9f3a-acde48001122', 'location': [1040, 4789]}

```

#### via Docker image (recommended)

```python
from jina import Flow
	
f = Flow().add(uses='jinahub+docker://SubtitleExtractor')
```

#### via source code

```python
from jina import Flow
	
f = Flow().add(uses='jinahub://SubtitleExtractor')
```

- To override `__init__` args & kwargs, use `.add(..., uses_with: {'key': 'value'})`
- To override class metas, use `.add(..., uses_metas: {'key': 'value})`
