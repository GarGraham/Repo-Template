import fs from "node:fs";
import yaml from "js-yaml";
import { buildFromConfig } from "./pipeline";

function loadCfg(path="mvp/ts/mvp.yaml"){
  return yaml.load(fs.readFileSync(path,"utf8"));
}

(async () => {
  const cfg = loadCfg();
  const p = buildFromConfig(cfg as any);
  await p.runOnce();
  console.log("MVP runOnce complete");
})();
