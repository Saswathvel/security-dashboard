'use client';

import { useState } from 'react';
import ScanInput from './ScanInput';

export default function Dashboard({ token }: { token: string }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [scanResults, setScanResults] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-semibold">🔐 Unified Security Dashboard</h1>
        <span className="text-sm text-gray-500">Token: {token}</span>
      </header>

      {/* Tabs */}
      <nav className="flex space-x-4 bg-gray-200 px-6 py-2">
        {['Overview', 'OSV-Scalibr', 'SBOM', 'CodeQL', 'Secrets'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab.toLowerCase())}
            className={`px-4 py-2 rounded-md ${
              activeTab === tab.toLowerCase()
                ? 'bg-blue-600 text-white'
                : 'bg-gray-300 text-gray-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* Tab Content */}
      <main className="flex-1 p-6 bg-white m-6 rounded-xl shadow-lg">
        {activeTab === 'overview' && (
          <>
            <ScanInput onScanComplete={setScanResults} />
            <p className="text-lg">Select a scan type and submit your codebase.</p>
          </>
        )}
        {activeTab === 'osv-scalibr' && (
          <pre className="bg-black text-white p-4 rounded overflow-x-auto text-sm">
            {scanResults?.osv ? JSON.stringify(scanResults.osv, null, 2) : 'Run a scan to see OSV results.'}
          </pre>
        )}
        {activeTab === 'sbom' && (
          <pre className="bg-black text-white p-4 rounded overflow-x-auto text-sm">
            {scanResults?.sbom ? JSON.stringify(scanResults.sbom, null, 2) : 'Run a scan to see SBOM results.'}
          </pre>
        )}
        {activeTab === 'codeql' && (
          <pre className="bg-black text-white p-4 rounded overflow-x-auto text-sm">
            {scanResults?.codeql ? JSON.stringify(scanResults.codeql, null, 2) : 'Run a scan to see CodeQL results.'}
          </pre>
        )}
        {activeTab === 'secrets' && (
          <pre className="bg-black text-white p-4 rounded overflow-x-auto text-sm">
            {scanResults?.secrets ? JSON.stringify(scanResults.secrets, null, 2) : 'Run a scan to see Gitleaks results.'}
          </pre>
        )}
      </main>
    </div>
  );
}
