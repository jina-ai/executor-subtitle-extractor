from pathlib import Path
from executors import SubtitleExtractor, MatchExtender, DPRReaderRanker

from jina import Document, DocumentArray


def test_subtitle_extractor():
    data_fn = Path(__file__).parents[1] / 'toy-data' / 'zvXkQkqd2I8.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    assert len(docs[0].chunks) == 231


def test_subtitle_extractor_case1():
    data_fn = Path(__file__).parent / 'toy-data' / 'data1.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    for c in docs[0].chunks:
        print(f'{c.location}: {c.text}')
    assert len(docs[0].chunks) == 3


def test_subtitle_extractor_case2():
    data_fn = Path(__file__).parent / 'toy-data' / 'data2.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    for c in docs[0].chunks:
        print(f'{c.location}: {c.text}')
    assert len(docs[0].chunks) == 13
