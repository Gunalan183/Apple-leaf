/**
 * Header Component
 * Beautiful application header with gradient and enhanced model info
 */

import { Activity, Info, Leaf, Sparkles, TrendingUp, Cpu } from 'lucide-react';
import { useState, useEffect } from 'react';
import { getModelInfo } from '../services/api';

const Header = () => {
  const [modelInfo, setModelInfo] = useState(null);
  const [showInfo, setShowInfo] = useState(false);

  useEffect(() => {
    getModelInfo()
      .then((data) => setModelInfo(data.model))
      .catch(() => setModelInfo(null));
  }, []);

  return (
    <header className="bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600 text-white shadow-xl relative overflow-hidden">
      {/* Decorative Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
          backgroundSize: '24px 24px'
        }}></div>
      </div>

      <div className="container mx-auto px-4 py-4 relative">
        <div className="flex items-center justify-between flex-wrap gap-3">
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <div className="bg-white/20 backdrop-blur-sm p-2.5 rounded-xl shadow-lg">
              <Leaf className="w-7 h-7 text-white drop-shadow-lg" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black drop-shadow-lg">Apple Leaf Disease Classifier</h1>
                <Sparkles className="w-4 h-4 text-yellow-300 animate-pulse" />
              </div>
              <p className="text-emerald-100 text-sm font-semibold flex items-center gap-1.5">
                <Activity className="w-3 h-3 animate-pulse" />
                AI-Powered Disease Detection System
              </p>
            </div>
          </div>
          
          {/* Model Info Button */}
          <button
            onClick={() => setShowInfo(!showInfo)}
            className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all duration-200 backdrop-blur-sm border border-white/30 shadow-md hover:shadow-lg"
          >
            <Info className="w-4 h-4" />
            <span className="font-bold text-sm">Model Info</span>
          </button>
        </div>

        {/* Expanded Model Info Card */}
        {showInfo && modelInfo && (
          <div className="mt-4 bg-white/15 backdrop-blur-md rounded-xl p-4 border border-white/30 shadow-xl animate-fadeIn">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Model Name */}
              <div className="bg-white/20 rounded-lg p-3 backdrop-blur-sm border border-white/30 hover:bg-white/25 transition-all duration-200">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="bg-gradient-to-br from-blue-500 to-indigo-500 p-1.5 rounded-md shadow-md">
                    <Cpu className="w-4 h-4 text-white" />
                  </div>
                  <p className="text-emerald-100 font-bold text-xs uppercase tracking-wide">Model</p>
                </div>
                <p className="text-white font-black text-base">{modelInfo.model_name}</p>
              </div>

              {/* Accuracy */}
              <div className="bg-white/20 rounded-lg p-3 backdrop-blur-sm border border-white/30 hover:bg-white/25 transition-all duration-200">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="bg-gradient-to-br from-green-500 to-emerald-500 p-1.5 rounded-md shadow-md">
                    <TrendingUp className="w-4 h-4 text-white" />
                  </div>
                  <p className="text-emerald-100 font-bold text-xs uppercase tracking-wide">Accuracy</p>
                </div>
                <p className="text-white font-black text-lg">{(modelInfo.validation_accuracy * 100).toFixed(1)}%</p>
              </div>

              {/* Classes */}
              <div className="bg-white/20 rounded-lg p-3 backdrop-blur-sm border border-white/30 hover:bg-white/25 transition-all duration-200">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="bg-gradient-to-br from-purple-500 to-pink-500 p-1.5 rounded-md shadow-md">
                    <Leaf className="w-4 h-4 text-white" />
                  </div>
                  <p className="text-emerald-100 font-bold text-xs uppercase tracking-wide">Classes</p>
                </div>
                <p className="text-white font-black text-base">{modelInfo.num_classes} Types</p>
              </div>

              {/* Device */}
              <div className="bg-white/20 rounded-lg p-3 backdrop-blur-sm border border-white/30 hover:bg-white/25 transition-all duration-200">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="bg-gradient-to-br from-orange-500 to-red-500 p-1.5 rounded-md shadow-md">
                    <Activity className="w-4 h-4 text-white" />
                  </div>
                  <p className="text-emerald-100 font-bold text-xs uppercase tracking-wide">Device</p>
                </div>
                <p className="text-white font-black text-base capitalize">{modelInfo.device}</p>
              </div>
            </div>

            {/* Additional Info Bar */}
            <div className="mt-3 flex items-center justify-center gap-2 text-emerald-100">
              <Sparkles className="w-3 h-3" />
              <p className="text-xs font-semibold">
                Model trained on {modelInfo.num_classes} disease classes with deep learning
              </p>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
