import json

def from_jsonp(jsonp_str, callback_name):
    """
    decode jsonp string
    """
    _jsonp_begin = r''+callback_name+'('
    _jsonp_end = r')'

    jsonp_str = jsonp_str.strip()

    if not jsonp_str.startswith(_jsonp_begin) or \
            not jsonp_str.endswith(_jsonp_end):
        raise ValueError('Invalid JSONP')

    return json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])
