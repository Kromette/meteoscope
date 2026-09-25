export interface WeatherObservation {
  timestamp: string
  temperature: number
  apparentTemperature: number
  humidity: number
  precipitation: number
  precipitationProbability: number
  weatherCode: number
  weatherDescription: string
  cloudCover: number
  windSpeed: number
  windDirection: number
  windGusts: number
}
