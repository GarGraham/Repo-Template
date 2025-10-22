import { z } from "zod";

export const DeviceReading = z.object({
  device_id: z.string(),
  timestamp: z.string(),
  temperatureC: z.number().optional(),
  status: z.enum(["OK","WARN","FAIL"]).optional(),
});

export type DeviceReading = z.infer<typeof DeviceReading>;
