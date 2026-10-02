const API_URL = 'http://localhost:8000'

export async function getMarineData(latitude: number, longitude: number) {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
  })

  const response = await fetch(`${API_URL}/marine?${params}`)

  if (!response.ok) {
    throw new Error(`Marine API error: ${response.status}`)
  }

  return response.json()
}
