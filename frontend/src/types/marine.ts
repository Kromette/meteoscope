export interface MarineHourlyData {
  timestamp: string

  wave_height: number
  wave_direction: number
  wave_period: number
  wave_peak_period: number | null

  wind_wave_height: number
  wind_wave_direction: number
  wind_wave_period: number
  wind_wave_peak_period: number | null

  swell_wave_height: number
  swell_wave_direction: number
  swell_wave_period: number
  swell_wave_peak_period: number | null

  secondary_swell_wave_height: number
  secondary_swell_wave_period: number
  secondary_swell_wave_direction: number

  tertiary_swell_wave_height: number | null
  tertiary_swell_wave_period: number | null
  tertiary_swell_wave_direction: number | null

  sea_level_height_msl: number
  sea_surface_temperature: number
  ocean_current_velocity: number
  ocean_current_direction: number
}

export interface MarineCurrentData {
  timestamp: string

  wave_height: number
  wave_direction: number
  wave_period: number
  wave_peak_period: number | null

  wind_wave_height: number
  wind_wave_direction: number
  wind_wave_period: number
  wind_wave_peak_period: number | null

  swell_wave_height: number
  swell_wave_direction: number
  swell_wave_period: number
  swell_wave_peak_period: number | null

  secondary_swell_wave_height: number
  secondary_swell_wave_period: number
  secondary_swell_wave_direction: number

  tertiary_swell_wave_height: number | null
  tertiary_swell_wave_period: number | null
  tertiary_swell_wave_direction: number | null

  sea_level_height_msl: number
  sea_surface_temperature: number
  ocean_current_velocity: number
  ocean_current_direction: number
}

export interface MarineMinutelyData {
  timestamp: string
  ocean_current_velocity: number
  ocean_current_direction: number
  sea_level_height_msl: number
}

export interface LocationData {
  latitude: number
  longitude: number
}

export interface MarineLocationData {
  location: LocationData
  date: string
  timezone: string
  marine_current: MarineCurrentData
  marine_minutely_15: MarineMinutelyData[]
  marine_hourly: MarineHourlyData[]
}

export interface MarineResponse {
  locations: MarineLocationData[]
}
