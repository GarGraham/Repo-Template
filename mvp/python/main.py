import yaml, pathlib
from mvp.python.app.pipeline import build_from_config

def load_cfg(path='mvp/python/mvp.yaml'):
    return yaml.safe_load(pathlib.Path(path).read_text())

if __name__ == "__main__":
    cfg = load_cfg()
    pipe = build_from_config(cfg)
    pipe.run_once()
    print("MVP run_once complete")
