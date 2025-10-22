import { DeviceReading } from "./models";
import { renameKeys, unitConvert, enumMap } from "./transforms";

export function parseDevicePayload(raw: any){
  let x = renameKeys(raw);
  x = unitConvert(x);
  x = enumMap(x);
  return DeviceReading.parse(x);
}
