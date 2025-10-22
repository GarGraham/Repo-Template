import fs from "node:fs";
import { DeviceReading } from "../src/models";

test("golden ok", () => {
  const data = JSON.parse(fs.readFileSync("mvp/ts/tests/golden/sample_ok.json","utf8"));
  const out = DeviceReading.parse({ device_id: data.deviceId, timestamp: data.timestamp, temperatureC: data.temperatureC, status: data.status });
  expect(out.device_id).toBeDefined();
});

test("golden bad fails", () => {
  const data = JSON.parse(fs.readFileSync("mvp/ts/tests/golden/sample_bad.json","utf8"));
  expect(()=> DeviceReading.parse({ device_id: data.deviceId, timestamp: data.timestamp })).toThrow();
});
