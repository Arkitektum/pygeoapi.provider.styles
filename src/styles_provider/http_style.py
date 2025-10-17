import logging
from typing import Dict, List
from urllib.parse import urljoin
import requests
from .base_style import BaseStyleProvider

LOGGER = logging.getLogger(__name__)


class HttpStyleProvider(BaseStyleProvider):
    def __init__(self, provider_def: Dict):
        BaseStyleProvider.__init__(self, provider_def)
        self._base_url: str = provider_def.get('base_url', '')

    def get_style_definition(self, style_id: str, format_: str) -> str | None:
        url = self._get_style_def_url(style_id, format_)

        if not url:
            return None

        try:
            response = requests.get(url)
            response.raise_for_status()

            return response.text
        except Exception as err:
            LOGGER.warning(f'Could not fetch style definition: {url}', err)
            return None

    def _get_style_def_url(self, style_id: str, format_: str) -> str | None:
        style = next(
            (style for style in self.styles if style['id'] == style_id), None)

        if not style:
            return None

        stylesheets: List[Dict] = style.get('stylesheets', [])
        stylesheet = next(
            (stylesheet for stylesheet in stylesheets if stylesheet['type'] == format_), None)

        if not stylesheet:
            return None

        path_str: str = stylesheet['path']

        return urljoin(self._base_url, path_str) if self._base_url else path_str
