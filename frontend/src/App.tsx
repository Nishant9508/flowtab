import { useState } from 'react'
import { Dashboard } from './components/Dashboard'
import { Setup } from './components/Setup'
import { Alerts } from './components/Alerts'

function App() {
  const [tab, setTab] = useState<'dashboard' | 'setup' | 'alerts'>('dashboard')

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm sticky top-0 z-10">
        <div className="text-xl font-black tracking-tight text-blue-900">flowtab</div>
        <div className="flex gap-4">
          <button 
            onClick={() => setTab('dashboard')} 
            className={`font-semibold px-3 py-1 rounded-md transition-colors ${tab === 'dashboard' ? 'bg-blue-50 text-blue-700' : 'text-gray-500 hover:bg-gray-50'}`}
          >
            Dashboard
          </button>
          <button 
            onClick={() => setTab('setup')}
            className={`font-semibold px-3 py-1 rounded-md transition-colors ${tab === 'setup' ? 'bg-blue-50 text-blue-700' : 'text-gray-500 hover:bg-gray-50'}`}
          >
            Setup
          </button>
        </div>
      </nav>
      
      <main className="p-6">
        {tab === 'dashboard' && <Dashboard />}
        {tab === 'setup' && <Setup />}
        {tab === "alerts" && <Alerts />}
      </main>
    </div>
  )
}

export default App
