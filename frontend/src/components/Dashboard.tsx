import type { WeatherObservation } from '../types/weather'
import LocationSelector from './LocationSelector'
import WeatherCard from './WeatherCard'
import DateSelector from './DateSelector'
import { useState } from 'react'

function Dashboard() {
  const currentWeather: WeatherObservation = {
    timestamp: '2026-09-24T14:00:00Z',
    temperature: 18,
    apparentTemperature: 20,
    humidity: 60,
    precipitation: 0,
    precipitationProbability: 0,
    weatherCode: 1,
    weatherDescription: 'Ensoleillé',
    cloudCover: 10,
    windSpeed: 15,
    windDirection: 180,
    windGusts: 25,
  }

  const weatherDetails = [
    { title: 'Humidité', value: '60%' },
    { title: 'Vent', value: '15 km/h' },
    { title: 'Pression', value: '1015 hPa' },
  ]

  const today = new Date()
  const possibleDates = Array.from({ length: 4 }, (_, i) => {
    const date = new Date(today)
    date.setDate(today.getDate() - (i + 1))
    return date.toISOString().split('T')[0]
  })
  const [selectedLocation, setSelectedLocation] = useState<string>('Paris')
  const [selectedDate, setSelectedDate] = useState<string>(possibleDates[0])

  return (
    <div className="space-y-6">
      <section className="rounded-2xl bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row">
          <LocationSelector
            locations={['Paris', 'Rennes', 'Lamballe', 'Erquy', 'Nantes']}
            selectedLocation={selectedLocation}
            onLocationChange={setSelectedLocation}
          />
          <DateSelector
            availableDates={possibleDates}
            selectedDate={selectedDate}
            onDateChange={setSelectedDate}
          />
        </div>
        <p className="mt-2 text-6xl font-bold tracking-tight text-slate-900">
          {currentWeather.temperature}°C
        </p>

        <p className="mt-2 text-slate-500">
          {currentWeather.weatherDescription}
        </p>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {weatherDetails.map((detail) => (
          <WeatherCard
            key={detail.title}
            title={detail.title}
            value={detail.value}
          />
        ))}
      </section>
    </div>
  )
}

export default Dashboard
