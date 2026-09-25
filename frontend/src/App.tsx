import Dashboard from './components/Dashboard'

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1 className="text-3xl font-bold text-blue-500">Meteoscope</h1>
        <span className="text-lg text-gray-600">Dashboard météo</span>
      </header>

      <Dashboard />
    </div>
  )
}

export default App
