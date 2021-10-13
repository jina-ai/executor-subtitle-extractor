from typing import Dict, Iterable, List, Optional, Tuple
import webvtt
import os

import numpy as np

from jina import Document, DocumentArray, Executor, requests


class SubtitleExtractor(Executor):
    @requests
    def extract(self, docs: Optional[DocumentArray], **kwargs):
        """
        Extract text from the `.vtt` files the use the heuristics to remove the duplicated text.
        :param docs:
        :param kwargs:
        :return:
        """
        if not docs:
            return
        for doc in docs:
            subtitles = self._load_subtitles(doc.uri)
            for idx, (beg, end, s) in enumerate(subtitles):
                len_tokens = len([t for t in s.split(' ')])
                if len_tokens <= 5:
                    continue
                chunk = Document(id=f'{doc.id}_{idx}', text=s)
                chunk.tags['beg_in_seconds'] = beg
                chunk.tags['end_in_seconds'] = end
                chunk.tags['vid'] = os.path.basename(doc.uri)
                chunk.location.append(int(beg * 1000))  # location in milliseconds
                chunk.location.append(int(end * 1000))  # location in milliseconds
                doc.chunks.append(chunk)

    def _load_subtitles(self, uri):
        beg = None
        is_last_cap_complete = True
        subtitles = []
        prev_parts = []
        for caption in webvtt.read(uri):
            # print(f'{repr(caption.text)}')
            cur_parts = [t for t in filter(lambda x: len(x.strip()) > 0, caption.text.split('\n'))]
            filtered_text = ' '.join(cur_parts)
            if len(cur_parts) == 1:
                if cur_parts[0] in prev_parts:
                    continue
            if len(cur_parts) > 1:
                if cur_parts[0] in prev_parts and is_last_cap_complete:
                    filtered_text = ' '.join(cur_parts[1:])
            is_cur_complete = True
            if is_last_cap_complete:
                beg = caption.start_in_seconds
            if caption.text.startswith(' \n') or caption.text.endswith('\n '):
                is_cur_complete = False
            if is_cur_complete:
                filtered_text = self.format_text(filtered_text)
                subtitles.append((beg, caption.end_in_seconds, filtered_text))
            is_last_cap_complete = is_cur_complete
            prev_parts = cur_parts
        return subtitles

    def format_text(self, text):
        return text.replace('gina', 'jina').replace('gene', 'jina')
