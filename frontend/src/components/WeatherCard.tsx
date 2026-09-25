function WeatherCard(props: { title: string; value: string }) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-6">
      <h2 className="text-sm font-medium text-slate-500">{props.title}</h2>
      <p className="mt-3 text-2xl font-semibold text-slate-900">
        {props.value}
      </p>
    </article>
  )
}

export default WeatherCard
