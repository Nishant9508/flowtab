import { useState, useEffect } from 'react';

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

export function Dashboard() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [flows, setFlows] = useState<Flow[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [filterCategory, setFilterCategory] = useState<string | null>(null)

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

  const filteredFlows = flows ? flows.filter(f => !filterCategory || f.charge_category === filterCategory) : []

  const handleExportCSV = () => {
    if (!flows) return
    const rows = [
      ["Sender Name", "Sender Type", "Receiver Name", "Receiver Type", "Category", "GB", "USD"],
      ...filteredFlows.map(f => [
        f.sender_name, f.sender_type, f.receiver_name, f.receiver_type, f.charge_category, f.gb.toFixed(4), f.usd.toFixed(2)
      ])
    ]
    const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n")
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", "flowtab_export.csv")
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">flowtab Data Transfer</h1>
          <p className="text-gray-500">Hourly bill reconciliation of flow logs</p>
        </div>
        <div className="flex gap-4">
          <button 
            onClick={generateDemo} 
            disabled={loading}
            className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold px-4 py-2 rounded shadow-sm border border-gray-300 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Refreshing...' : 'Reset Demo Data'}
          </button>
        </div>
      </div>

      {summary && summary.total_gb > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-blue-500 transition-all hover:shadow-md">
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1 flex items-center gap-1">Total Cost</h2>
              <div className="text-3xl font-bold text-gray-900">${summary.total_usd.toFixed(2)}</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-green-500 transition-all hover:shadow-md">
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">Total Volume</h2>
              <div className="text-3xl font-bold text-gray-900">{summary.total_gb.toFixed(2)} GB</div>
            </div>
            
            {/* Category breakdown clickable filters */}
            <div className="col-span-2 bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex flex-col justify-center">
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-2">Cost By Category</h2>
              <div className="flex flex-wrap gap-2">
                <button 
                  onClick={() => setFilterCategory(null)}
                  className={`px-3 py-1 text-sm rounded-full transition-colors ${!filterCategory ? 'bg-blue-100 text-blue-800 ring-2 ring-blue-300 font-semibold' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                >
                  All
                </button>
                {Object.entries(summary.by_category).sort((a,b) => b[1] - a[1]).map(([cat, usd]) => (
                  <button 
                    key={cat}
                    onClick={() => setFilterCategory(cat)}
                    className={`px-3 py-1 text-sm rounded-full transition-colors ${filterCategory === cat ? 'bg-blue-100 text-blue-800 ring-2 ring-blue-300 font-semibold' : 'bg-gray-100 text-gray-600 hover:bg-gray-200 flex items-center gap-2'}`}
                  >
                    <span>{cat}</span>
                    <span className={`text-xs ${filterCategory === cat ? 'text-blue-800 font-bold' : 'text-gray-500'}`}>${usd.toFixed(2)}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="flex justify-between items-center bg-gray-50 px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-800">
                Network Flows {filterCategory && <span className="text-blue-600 ml-2">› {filterCategory}</span>}
              </h2>
              <button 
                onClick={handleExportCSV}
                className="text-sm bg-white border border-gray-300 hover:bg-gray-50 px-3 py-1.5 rounded shadow-sm text-gray-700 font-medium transition-colors"
                title="Download current view as CSV"
              >
                Export CSV
              </button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Sender</th>
                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Receiver</th>
                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</th>
                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Volume (GB)</th>
                    <th className="p-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Cost (USD)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredFlows.sort((a,b) => b.usd - a.usd).map((f, i) => (
                    <tr key={i} className="hover:bg-blue-50/50 transition-colors group">
                      <td className="p-4">
                        <div className="font-medium text-gray-900 group-hover:text-blue-700 transition-colors">{f.sender_name}</div>
                        <div className="text-xs text-gray-500 mt-1 inline-flex items-center px-1.5 py-0.5 rounded-sm bg-gray-100 border border-gray-200">{f.sender_type}</div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <svg className="w-4 h-4 text-gray-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                          <div>
                            <div className="font-medium text-gray-900 group-hover:text-blue-700 transition-colors">{f.receiver_name}</div>
                            <div className="text-xs text-gray-500 mt-1 inline-flex items-center px-1.5 py-0.5 rounded-sm bg-gray-100 border border-gray-200">{f.receiver_type}</div>
                          </div>
                        </div>
                      </td>
                      <td className="p-4">
                        <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                          {f.charge_category}
                        </span>
                      </td>
                      <td className="p-4 text-right">
                        <span className="font-mono text-sm text-gray-600">{f.gb.toFixed(4)}</span>
                      </td>
                      <td className="p-4 text-right">
                        <span className="font-mono text-sm font-semibold text-gray-900">${f.usd.toFixed(2)}</span>
                      </td>
                    </tr>
                  ))}
                  {filteredFlows.length === 0 && (
                    <tr>
                      <td colSpan={5} className="p-12 text-center text-gray-500">No flows match the selected filter.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 text-blue-500 mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Data Available</h2>
          <p className="text-gray-500 max-w-md mx-auto mb-6">Start by generating some synthetic demo data to see how flowtab visualizes network costs.</p>
          <button 
            onClick={generateDemo}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2.5 rounded-lg shadow-sm disabled:opacity-50 transition-colors"
          >
            {loading ? 'Generating...' : 'Generate Demo Data'}
          </button>
        </div>
      )}
    </div>
  )
}
