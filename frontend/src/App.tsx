import { useEffect, useState } from 'react'

type Summary = {
  total_gb: number;
  total_usd: number;
  by_category: Record<string, number>;
}

type Flow = {
  sender_type: string;
  sender_name: string;
  receiver_type: string;
  receiver_name: string;
  route: string;
  charge_category: string;
  gb: number;
  usd: number;
}

function App() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [flows, setFlows] = useState<Flow[] | null>(null)
  const [loading, setLoading] = useState(false)

  const generateDemo = async () => {
    setLoading(true)
    await fetch('/api/v1/demo/generate', { method: 'POST', body: JSON.stringify({}), headers: { 'Content-Type': 'application/json' } })
    loadData()
  }

  const loadData = async () => {
    setLoading(true)
    try {
      const sumRes = await fetch('/api/v1/network/summary')
      const sumData = await sumRes.json()
      setSummary(sumData)

      const devRes = await fetch('/api/v1/network/flows')
      const devData = await devRes.json()
      setFlows(devData.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [])

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-blue-900">flowtab</h1>
          <button 
            onClick={generateDemo} 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow disabled:opacity-50"
          >
            Generate Demo Data
          </button>
        </div>

        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded shadow border-t-4 border-blue-500">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-widest mb-1">Total Cost</h2>
              <div className="text-3xl font-bold">${summary.total_usd.toFixed(2)}</div>
            </div>
            <div className="bg-white p-6 rounded shadow border-t-4 border-green-500">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-widest mb-1">Total Volume</h2>
              <div className="text-3xl font-bold">{summary.total_gb.toFixed(2)} GB</div>
            </div>
            <div className="bg-white p-6 rounded shadow border-t-4 border-purple-500">
                <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-widest mb-1">Top Category</h2>
                <div className="text-xl font-bold truncate">
                  {Object.entries(summary.by_category).sort((a,b) => b[1] - a[1])[0]?.[0] || 'N/A'}
                </div>
            </div>
          </div>
        )}

        {flows && (
          <div className="bg-white p-6 rounded shadow overflow-x-auto">
            <h2 className="text-xl font-bold mb-4">Network Flows</h2>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-100 border-b">
                  <th className="p-3 text-sm font-bold text-gray-700">Sender</th>
                  <th className="p-3 text-sm font-bold text-gray-700">Receiver</th>
                  <th className="p-3 text-sm font-bold text-gray-700">Category</th>
                  <th className="p-3 text-sm font-bold text-gray-700 text-right">Volume (GB)</th>
                  <th className="p-3 text-sm font-bold text-gray-700 text-right">Cost (USD)</th>
                </tr>
              </thead>
              <tbody>
                {flows.sort((a,b) => b.usd - a.usd).map((f, i) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="p-3">
                      <div className="font-semibold">{f.sender_name}</div>
                      <div className="text-xs text-gray-500 bg-gray-200 inline-block px-1 rounded">{f.sender_type}</div>
                    </td>
                    <td className="p-3 flex items-center gap-2">
                      <span className="text-gray-400">→</span>
                      <div>
                        <div className="font-semibold">{f.receiver_name}</div>
                        <div className="text-xs text-gray-500 bg-gray-200 inline-block px-1 rounded">{f.receiver_type}</div>
                      </div>
                    </td>
                    <td className="p-3 text-sm">{f.charge_category}</td>
                    <td className="p-3 text-right font-mono text-sm">{f.gb.toFixed(4)}</td>
                    <td className="p-3 text-right font-mono text-sm font-semibold">${f.usd.toFixed(2)}</td>
                  </tr>
                ))}
                {flows.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-8 text-center text-gray-500">No data available. Click Generate Demo Data.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
