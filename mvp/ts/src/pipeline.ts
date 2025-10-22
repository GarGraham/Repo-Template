import { MqttSource } from "./adapters/source/mqtt";
import { HttpSink } from "./adapters/sink/http_push";
import { parseDevicePayload } from "./parse";

export class Pipeline {
  source: any; sink: any;
  constructor(source:any, sink:any){ this.source=source; this.sink=sink; }
  async runOnce(){
    for (const raw of this.source.stream()){
      const reading = parseDevicePayload(raw);
      await this.sink.send(reading);
    }
  }
}

export function buildFromConfig(cfg:any){
  return new Pipeline(new MqttSource(cfg.source), new HttpSink(cfg.sink));
}
