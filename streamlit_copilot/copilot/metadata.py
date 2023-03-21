import logging
from typing import List

from streamlit_copilot.copilot.model import CodeExtractor


logger = logging.getLogger(__name__)


def extract_data_loading_snippets(code: str) -> List[str]:
    extractor = CodeExtractor().run(code, "Extract the data loading code.")
    logger.debug(f"Extracted snippets:\n\n{extractor}")
    return extractor