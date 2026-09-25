function LocationSelector({
  locations,
  selectedLocation,
  onLocationChange,
}: {
  locations: string[]
  selectedLocation: string
  onLocationChange: (location: string) => void
}) {
  return (
    <div className="location-selector">
      <label htmlFor="location">Choose a location : </label>
      <select
        id="location"
        name="location"
        value={selectedLocation}
        onChange={(e) => onLocationChange(e.target.value)}
      >
        {locations.map((location) => (
          <option key={location} value={location}>
            {location}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LocationSelector
