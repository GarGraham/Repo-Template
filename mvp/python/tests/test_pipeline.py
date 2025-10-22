from mvp.python.main import load_cfg
from mvp.python.app.pipeline import build_from_config

def test_pipeline_smoke():
    cfg = load_cfg()
    p = build_from_config(cfg)
    p.run_once()
