import { useEffect, useRef } from 'react'

import { Map, Marker, setWorkerUrl } from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'
import 'maplibre-gl/dist/maplibre-gl.css'

setWorkerUrl(workerUrl)

interface MapSelectorProps {
  latitude: number
  longitude: number
  onLocationSelect: (latitude: number, longitude: number) => void
}

function MapSelector({
  latitude,
  longitude,
  onLocationSelect,
}: MapSelectorProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null)
  const map = useRef<Map | null>(null)
  const marker = useRef<Marker | null>(null)

  useEffect(() => {
    if (!mapContainer.current) {
      return
    }

    map.current = new Map({
      container: mapContainer.current,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [longitude, latitude],
      zoom: 8,
    })

    map.current.on('click', (event) => {
      const { lat, lng } = event.lngLat

      marker.current?.remove()

      marker.current = new Marker().setLngLat([lng, lat]).addTo(map.current!)

      onLocationSelect(lat, lng)
    })

    return () => {
      map.current?.remove()
      map.current = null
    }
  }, [])

  return <div ref={mapContainer} className="h-[500px] w-full rounded-xl" />
}

export default MapSelector
