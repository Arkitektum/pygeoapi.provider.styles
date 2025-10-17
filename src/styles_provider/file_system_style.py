from typing import Dict, List
from pathlib import Path
from .base_style import BaseStyleProvider


class FileSystemStyleProvider(BaseStyleProvider):
    def __init__(self, provider_def: Dict):
        BaseStyleProvider.__init__(self, provider_def)
        self._base_dir: str = provider_def.get('base_dir', '')

    def get_style_definition(self, style_id: str, format_: str) -> str | None:
        path = self._get_style_def_path(style_id, format_)

        if not path:
            return None

        with open(path, 'r') as file:
            return file.read()

    def _get_style_def_path(self, style_id: str, format_: str) -> Path | None:
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

        path = Path(self._base_dir).joinpath(
            path_str) if self._base_dir else Path(path_str)

        if not path.exists():
            return None

        return path
