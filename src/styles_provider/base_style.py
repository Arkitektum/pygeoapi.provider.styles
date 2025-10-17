from typing import Dict, List, Any

STYLESHEET_TYPES = {
    'mapbox': {
        'title': 'Mapbox Style',
        'mime_type': 'application/vnd.mapbox.style+json',
        'version': '8',
        'spec': 'https://docs.mapbox.com/style-spec/guides',
        'format': 'mapbox'
    },
    'se11': {
        'title': 'OGC SE',
        'mime_type': 'application/vnd.ogc.se+xml;version=1.1',
        'version': '1.1',
        'spec': 'https://www.ogc.org/standards/se',        
        'format': 'se11'
    },
    'sld10': {
        'title': 'OGC SLD',
        'mime_type': 'application/vnd.ogc.sld+xml;version=1.0',
        'version': '1.0',
        'spec': 'https://www.ogc.org/standards/sld',
        'format': 'sld10'
    }
}


class BaseStyleProvider:
    def __init__(self, provider_def: Dict):
        self.styles: List[Dict[str, Any]] = provider_def['styles']
        self.server_url = provider_def['server_url']

    def get_styles(self) -> Dict[str, Any]:
        styles: List[Dict] = []

        for style in self.styles:
            id: str = style['id']

            links = [
                {
                    'rel': 'describedby',
                    'title': 'Style metadata',
                    'href': f'{self.server_url}/styles/{id}/metadata'
                },
                {
                    'rel': 'stylesheet',
                    'type': 'text/html',
                    'title': 'Web map using the style',
                    'href': f'{self.server_url}/styles/{id}?f=html'
                }
            ]

            stylesheets: List[Dict] = style['stylesheets']

            for styleheet in stylesheets:
                type = styleheet['type']

                links.append({
                    'rel': 'stylesheet',
                    'type': STYLESHEET_TYPES[type]['mime_type'],
                    'title': f'Style in {STYLESHEET_TYPES[type]["title"]} format',
                    'href': f'{self.server_url}/styles/{id}?f={STYLESHEET_TYPES[type]["format"]}'
                })

            styles.append({
                'id': id,
                'title': style.get('title'),
                'links': links
            })

        return {
            'styles': styles
        }

    def get_style(self, style_id: str) -> Dict[str, Any] | None:
        styles: List[Dict] = self.get_styles().get('styles', [])
        style = next(
            (style for style in styles if style['id'] == style_id), None)

        return style
    
    def get_style_metadata(self, style_id: str) -> Dict[str, Any] | None:
        style = next(
            (style for style in self.styles if style['id'] == style_id), None)

        if not style:
            return None
        
        metadata = {
            'id': style['id'],
            'title': style['title']
        }

        description = style.get('description')

        if description:
            metadata['description'] = description

        keywords = style.get('keywords')

        if keywords:
            metadata['keywords'] = keywords
            
        metadata['scope'] = 'style'

        version = style.get('version')

        if version:
            metadata['version'] = version

        stylesheets: List[Dict] = style['stylesheets']
        metadata['stylesheets'] = []

        for styleheet in stylesheets:
            type = STYLESHEET_TYPES[styleheet['type']]
            
            metadata['stylesheets'].append({
                'title': type['title'],
                'version': type['version'],
                'specification': type['spec'],
                'native': styleheet['native'],
                'link': {
                    'href': f'{self.server_url}/styles/{style_id}?f={type["format"]}',
                    'rel': 'stylesheet',
                    'type': type['mime_type']
                }
            })

        layers: List[Dict] = style['layers']
        metadata['layers'] = []

        for layer in layers:           
            metadata['layers'].append({
                'id': layer['id'],
                'type': layer['type']
            })

        return metadata  

    def get_style_definition(self, style_id: str, format_: str) -> str | None:
        raise NotImplementedError()

    def get_style_preview(self, style_id: str):
        raise NotImplementedError()
