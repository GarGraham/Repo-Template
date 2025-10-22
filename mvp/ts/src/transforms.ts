import fs from "node:fs";
import yaml from "js-yaml";

function loadMap(path="mvp/ts/config/mapping.yaml"): any {
  return yaml.load(fs.readFileSync(path,"utf8")) as any;
}

export function renameKeys(d: any, mappingPath?: string){
  const m = loadMap(mappingPath || "mvp/ts/config/mapping.yaml");
  const ren = m.rename || {};
  const out: any = {};
  Object.entries(d).forEach(([k,v])=> out[ren[k] ?? k] = v);
  return out;
}

export function unitConvert(d: any){ return d; }
export function enumMap(d: any){
  const m = loadMap().enums || {};
  if (d.status && m.status) d.status = m.status[d.status] ?? d.status;
  return d;
}
