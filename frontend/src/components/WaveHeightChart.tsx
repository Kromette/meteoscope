import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { MarineHourlyData } from '../types/marine'

interface WaveHeightChartProps {
  data: MarineHourlyData[]
}

export function WaveHeightChart({ data }: WaveHeightChartProps) {
  const chartData = data.map((observation) => ({
    time: new Date(observation.timestamp).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
    }),
    waveHeight: observation.wave_height,
  }))

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="time" />

          <YAxis
            label={{
              value: 'Hauteur (m)',
              angle: -90,
              position: 'insideLeft',
            }}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="waveHeight"
            name="Hauteur des vagues"
            unit=" m"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
