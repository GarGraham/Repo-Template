export class MqttSource {
  cfg: any;
  constructor(cfg:any){ this.cfg = cfg; }
  *stream(){
    // Stubbed generator example
    yield { deviceId:"demo-1", timestamp:"2025-01-01T00:00:00Z", temperatureC:22.1, status:"OK" };
  }
}
