type DateSelectorProps = {
  availableDates: string[]
  selectedDate: string
  onDateChange: (date: string) => void
}

function DateSelector({
  availableDates,
  selectedDate,
  onDateChange,
}: DateSelectorProps) {
  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onDateChange(event.target.value)
  }

  return (
    <div className="date-selector">
      <label htmlFor="date">Choose a date :</label>
      <input
        type="date"
        id="date"
        min={availableDates[availableDates.length - 1]}
        max={availableDates[0]}
        value={selectedDate}
        onChange={handleDateChange}
      />
    </div>
  )
}

export default DateSelector
