import { useState, useEffect } from 'react';

type Insight = {
  title: string;
  description: string;
  severity: string;
  cost_impact: number;
  vpc: string;
}

export function Alerts() {
  const [insights, setInsights] = useState<Insight[] | null>(null)
  
  useEffect(() => {
    fetch('/api/v1/network/insights')
      .then(res => res.json())
      .then(data => setInsights(data.insights))
  }, [])
  
  return (
    <div className="max-w-6xl mx-auto py-8">
      <h2 className="text-2xl font-bold mb-6">Optimization Insights</h2>
      
      {insights && insights.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {insights.map((ins, i) => (
            <div key={i} className={`bg-white p-6 rounded shadow border-l-4 ${ins.severity === 'high' ? 'border-l-red-500' : ins.severity === 'medium' ? 'border-l-yellow-500' : 'border-l-green-500'}`}>
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{ins.title}</h3>
                {ins.cost_impact > 0 && (
                  <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded font-mono font-bold border border-red-200">
                    Impact: ${ins.cost_impact.toFixed(2)}
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-500 mb-2">VPC: {ins.vpc}</p>
              <p className="text-gray-700">{ins.description}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white p-8 rounded shadow text-center text-gray-500">
          No insights available.
        </div>
      )}
    </div>
  )
}
