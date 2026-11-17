/**
 * Home Page
 * Beautiful main application page with enhanced UI
 */

import { useState } from 'react';
import { Loader2, AlertCircle, RefreshCw, Sparkles, Target, Brain, BarChart3 } from 'lucide-react';
import ImageUploader from '../components/ImageUploader';
import PredictionResult from '../components/PredictionResult';
import { predictDisease } from '../services/api';

const Home = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setPrediction(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setIsLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await predictDisease(selectedImage);
      setPrediction(result.prediction);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to analyze image. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-emerald-50/30">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Hero Instructions Card */}
        <div className="bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 rounded-3xl p-8 mb-10 shadow-2xl text-white relative overflow-hidden">
          {/* Decorative Background */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
              backgroundSize: '24px 24px'
            }}></div>
          </div>

          <div className="relative">
            <div className="flex items-center gap-3 mb-4">
              <Sparkles className="w-8 h-8 animate-pulse" />
              <h2 className="text-3xl font-black">How It Works</h2>
            </div>
            <div className="grid md:grid-cols-3 gap-6 mt-6">
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-5 border border-white/30">
                <div className="bg-gradient-to-br from-emerald-500 to-green-500 w-12 h-12 rounded-xl flex items-center justify-center text-2xl font-black mb-3 shadow-lg">
                  1
                </div>
                <h3 className="font-bold text-lg mb-2">Upload Image</h3>
                <p className="text-blue-100 text-sm">Take or upload a clear photo of an apple leaf</p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-5 border border-white/30">
                <div className="bg-gradient-to-br from-orange-500 to-red-500 w-12 h-12 rounded-xl flex items-center justify-center text-2xl font-black mb-3 shadow-lg">
                  2
                </div>
                <h3 className="font-bold text-lg mb-2">AI Analysis</h3>
                <p className="text-blue-100 text-sm">Our AI model analyzes the leaf in seconds</p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-5 border border-white/30">
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 w-12 h-12 rounded-xl flex items-center justify-center text-2xl font-black mb-3 shadow-lg">
                  3
                </div>
                <h3 className="font-bold text-lg mb-2">Get Results</h3>
                <p className="text-blue-100 text-sm">View diagnosis with treatment recommendations</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Upload Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-3xl shadow-2xl p-8 border-2 border-gray-100">
              <div className="flex items-center gap-3 mb-6">
                <div className="bg-gradient-to-br from-emerald-500 to-teal-500 p-3 rounded-xl shadow-lg">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-3xl font-black text-gray-900">Upload Leaf Image</h2>
              </div>
              
              <ImageUploader 
                onImageSelect={handleImageSelect}
                isLoading={isLoading}
              />

              {/* Action Buttons */}
              {selectedImage && !prediction && (
                <div className="mt-8 flex gap-4">
                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading}
                    className="flex-1 flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-emerald-500 to-teal-500 text-white rounded-2xl hover:from-emerald-600 hover:to-teal-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-black text-lg shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-6 h-6 animate-spin" />
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-6 h-6" />
                        <span>Analyze Leaf</span>
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleReset}
                    disabled={isLoading}
                    className="px-8 py-4 bg-gray-200 text-gray-700 rounded-2xl hover:bg-gray-300 disabled:opacity-50 transition-all duration-200 font-bold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center gap-2"
                  >
                    <RefreshCw className="w-5 h-5" />
                    <span>Reset</span>
                  </button>
                </div>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-6 bg-gradient-to-br from-red-50 to-rose-50 border-2 border-red-200 rounded-2xl p-6 flex items-start gap-4 shadow-lg animate-fadeIn">
                <div className="bg-gradient-to-br from-red-500 to-rose-500 p-3 rounded-xl shadow-lg flex-shrink-0">
                  <AlertCircle className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="font-black text-red-900 text-lg">Error Occurred</p>
                  <p className="text-red-700 font-semibold mt-1">{error}</p>
                </div>
              </div>
            )}

            {/* Results Section */}
            {prediction && (
              <div className="mt-8 bg-white rounded-3xl shadow-2xl p-8 border-2 border-gray-100">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-purple-500 to-pink-500 p-3 rounded-xl shadow-lg">
                      <BarChart3 className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-3xl font-black text-gray-900">Analysis Results</h2>
                  </div>
                  <button
                    onClick={handleReset}
                    className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-gray-200 to-gray-300 text-gray-700 rounded-xl hover:from-gray-300 hover:to-gray-400 transition-all duration-200 font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                  >
                    <RefreshCw className="w-4 h-4" />
                    <span>New Analysis</span>
                  </button>
                </div>
                <PredictionResult prediction={prediction} />
              </div>
            )}
          </div>

          {/* Right Column - Info Cards */}
          <div className="space-y-6">
            {/* AI Model Info */}
            <div className="bg-gradient-to-br from-purple-500 via-indigo-500 to-blue-500 rounded-3xl p-6 shadow-2xl text-white">
              <div className="flex items-center gap-3 mb-4">
                <Brain className="w-8 h-8" />
                <h3 className="text-2xl font-black">AI Technology</h3>
              </div>
              <div className="space-y-3">
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4 border border-white/30">
                  <p className="font-bold mb-1">DenseNet121</p>
                  <p className="text-sm text-blue-100">Deep convolutional neural network</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4 border border-white/30">
                  <p className="font-bold mb-1">95%+ Accuracy</p>
                  <p className="text-sm text-blue-100">Validated on test dataset</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4 border border-white/30">
                  <p className="font-bold mb-1">3 Disease Classes</p>
                  <p className="text-sm text-blue-100">Healthy, Rust, Scab detection</p>
                </div>
              </div>
            </div>

            {/* Disease Info */}
            <div className="bg-white rounded-3xl p-6 shadow-2xl border-2 border-gray-100">
              <h3 className="text-2xl font-black text-gray-900 mb-4">Disease Types</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 rounded-full bg-gradient-to-br from-emerald-500 to-green-500 mt-1.5 flex-shrink-0 shadow-lg"></div>
                  <div>
                    <p className="font-bold text-gray-900">Healthy</p>
                    <p className="text-sm text-gray-600">No disease detected</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 rounded-full bg-gradient-to-br from-orange-500 to-amber-500 mt-1.5 flex-shrink-0 shadow-lg"></div>
                  <div>
                    <p className="font-bold text-gray-900">Apple Rust</p>
                    <p className="text-sm text-gray-600">Orange spots on leaves</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 rounded-full bg-gradient-to-br from-red-500 to-rose-500 mt-1.5 flex-shrink-0 shadow-lg"></div>
                  <div>
                    <p className="font-bold text-gray-900">Apple Scab</p>
                    <p className="text-sm text-gray-600">Dark scabby lesions</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-br from-emerald-500 via-green-500 to-teal-500 rounded-3xl p-6 shadow-2xl text-white">
              <h3 className="text-2xl font-black mb-4">Quick Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-semibold">Speed</span>
                  <span className="font-black text-xl">&lt;3 sec</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-semibold">Accuracy</span>
                  <span className="font-black text-xl">95%+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-semibold">Classes</span>
                  <span className="font-black text-xl">3 types</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
