export function toExternalCamel(obj: any){
  if (obj == null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(toExternalCamel);
  const out: any = {};
  for (const [k,v] of Object.entries(obj)){
    const camel = k.replace(/_([a-z])/g, (_,c)=> c.toUpperCase());
    out[camel] = toExternalCamel(v as any);
  }
  return out;
}
