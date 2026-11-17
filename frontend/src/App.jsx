/**
 * Main App Component
 * Root component with routing and layout
 */

import { useEffect, useState } from 'react';
import { AlertCircle } from 'lucide-react';
import Header from './components/Header';
import Home from './pages/Home';
import { checkHealth } from './services/api';
import './App.css';

function App() {
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend health on mount
    checkHealth()
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('disconnected'));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Backend Status Warning */}
      {backendStatus === 'disconnected' && (
        <div className="bg-yellow-50 border-b border-yellow-200 px-4 py-3">
          <div className="container mx-auto flex items-center space-x-2 text-yellow-800">
            <AlertCircle className="w-5 h-5" />
            <p className="text-sm">
              <strong>Backend Disconnected:</strong> Please ensure the backend server is running at http://localhost:8000
            </p>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="pb-12">
        <Home />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>GAN-Sim-GAN © 2026 • Apple Leaf Disease Classification</p>
          <p className="mt-1">
            Powered by DenseNet121 • Research-based AI Model
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
