import { useEffect, useState } from 'react'

function App() {
  const [health, setHealth] = useState<string>('checking...')

  useEffect(() => {
    fetch('/api/v1/health')
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(err => setHealth('error: ' + err.message))
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">flowtab</h1>
      <p>Backend status: {health}</p>
    </div>
  )
}

export default App
