export class HttpSink {
  url: string;
  constructor(cfg:any){ this.url = cfg.url; }
  async send(payload: any){
    // Using undici would be typical; keep Node fetch for simplicity if enabled
    const res = await fetch(this.url, { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(payload) });
    return res.status;
  }
}
