import yaml, pathlib

def load_mapping(path='mvp/python/config/mapping.yaml'):
    return yaml.safe_load(pathlib.Path(path).read_text())

def rename_keys(d: dict, mapping_path=None):
    m = load_mapping(mapping_path or 'mvp/python/config/mapping.yaml')
    ren = m.get('rename', {}); out = {}
    for k,v in d.items():
        out[ren.get(k,k)] = v
    return out

def unit_convert(d: dict):
    # extend as needed; placeholder
    return d

def enum_map(d: dict):
    m = load_mapping().get('enums', {})
    if 'status' in d and 'status' in m:
        d['status'] = m['status'].get(str(d['status']), d['status'])
    return d
