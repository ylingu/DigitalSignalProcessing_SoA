export interface FileRecord {
  filename: string
  url: string
}
export interface UploadConfig {
  action: string
  extraData?: Record<string, number | boolean> | string
}
