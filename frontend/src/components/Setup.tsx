import { useState, useEffect } from 'react';

type Scope = {
  account_id: string;
  regions: string[];
  vpcs: {
    vpc_id: string;
    region: string;
    name: string;
    mode: string;
    is_enabled: boolean;
  }[]
}

export function Setup() {
  const [scopes, setScopes] = useState<Scope[] | null>(null)
  
  useEffect(() => {
    fetch('/api/v1/network/scopes')
      .then(res => res.json())
      .then(data => setScopes(data.accounts))
  }, [])
  
  return (
    <div className="max-w-6xl mx-auto py-8">
      <h2 className="text-2xl font-bold mb-6">Environment Setup & Probes</h2>
      
      {scopes && scopes.length > 0 ? (
        <div className="flex flex-col gap-6">
          {scopes.map(s => (
            <div key={s.account_id} className="bg-white p-6 rounded shadow border">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span className="text-gray-500">Account</span> {s.account_id}
              </h3>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse mt-4">
                  <thead>
                    <tr className="bg-gray-50 border-b border-t text-sm text-gray-500">
                      <th className="p-3 font-semibold">Region</th>
                      <th className="p-3 font-semibold">VPC</th>
                      <th className="p-3 font-semibold">Name</th>
                      <th className="p-3 font-semibold text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {s.vpcs.map(v => (
                      <tr key={v.vpc_id} className="border-b">
                        <td className="p-3">{v.region}</td>
                        <td className="p-3 font-mono">{v.vpc_id}</td>
                        <td className="p-3">{v.name}</td>
                        <td className="p-3 text-center">
                          {v.is_enabled ? (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold">Enabled ({v.mode})</span>
                          ) : (
                            <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs font-bold">Disabled</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white p-8 rounded shadow text-center text-gray-500">
          No accounts discovered yet. Generate demo data to see.
        </div>
      )}
    </div>
  )
}
