/**
 * Prediction Result Component
 * Beautiful result cards with visual confidence meters
 */

import { CheckCircle, AlertCircle, AlertTriangle, Leaf, TrendingUp, Activity, Sparkles } from 'lucide-react';

const PredictionResult = ({ prediction }) => {
  if (!prediction) return null;

  const { class: className, class_display, confidence, probabilities, is_diseased } = prediction;

  // Enhanced disease configuration with gradients and animations
  const diseaseConfig = {
    healthy: {
      title: 'Healthy Leaf',
      description: 'The leaf appears to be in excellent condition with no signs of disease detected.',
      icon: CheckCircle,
      color: 'emerald',
      gradient: 'from-emerald-500 via-green-500 to-teal-500',
      bgGradient: 'from-emerald-50 via-green-50 to-teal-50',
      borderColor: 'border-emerald-200',
      glowColor: 'shadow-emerald-500/20',
      recommendations: [
        'Continue regular monitoring schedule',
        'Maintain optimal irrigation practices',
        'Ensure proper nutrient management',
        'Keep documenting leaf health',
      ],
    },
    rust: {
      title: 'Apple Rust Detected',
      description: 'Rust is a fungal disease causing orange or rust-colored spots. Early detection enables effective treatment.',
      icon: AlertTriangle,
      color: 'orange',
      gradient: 'from-orange-500 via-amber-500 to-yellow-500',
      bgGradient: 'from-orange-50 via-amber-50 to-yellow-50',
      borderColor: 'border-orange-200',
      glowColor: 'shadow-orange-500/20',
      recommendations: [
        'Apply recommended fungicide treatment',
        'Remove and dispose of infected leaves',
        'Improve air circulation around trees',
        'Avoid overhead watering methods',
      ],
    },
    scab: {
      title: 'Apple Scab Detected',
      description: 'Scab is a serious fungal disease causing dark lesions. Immediate action is recommended to prevent spread.',
      icon: AlertCircle,
      color: 'red',
      gradient: 'from-red-500 via-rose-500 to-pink-500',
      bgGradient: 'from-red-50 via-rose-50 to-pink-50',
      borderColor: 'border-red-200',
      glowColor: 'shadow-red-500/20',
      recommendations: [
        'Apply appropriate fungicide immediately',
        'Remove all fallen leaves from ground',
        'Prune to improve air circulation',
        'Consider disease-resistant varieties',
      ],
    },
  };

  const config = diseaseConfig[className] || diseaseConfig.healthy;
  const Icon = config.icon;

  // Sort probabilities for better visualization
  const sortedProbs = Object.entries(probabilities)
    .sort(([, a], [, b]) => b - a)
    .map(([name, prob]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      className: name.toLowerCase(),
      value: prob,
    }));

  return (
    <div className="mt-6 space-y-5 animate-fadeIn">
      {/* Compact Result Card */}
      <div className={`relative bg-gradient-to-br ${config.bgGradient} rounded-2xl p-5 shadow-xl border-2 ${config.borderColor} backdrop-blur-sm overflow-hidden`}>
        {/* Decorative Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0)',
            backgroundSize: '24px 24px'
          }}></div>
        </div>

        <div className="relative">
          <div className="flex items-start gap-4 mb-4">
            <div className={`bg-gradient-to-br ${config.gradient} p-3 rounded-xl shadow-lg ${config.glowColor} transform hover:scale-105 transition-transform duration-300`}>
              <Icon className="w-8 h-8 text-white drop-shadow-lg" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="text-2xl font-black text-gray-900">{config.title}</h3>
                <Sparkles className={`w-4 h-4 text-${config.color}-500 animate-pulse`} />
              </div>
              <p className="text-gray-700 text-sm leading-relaxed font-medium">{config.description}</p>
            </div>
          </div>

          {/* Compact Confidence Display */}
          <div className="mt-4 bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-white/50 shadow-inner">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Activity className={`w-5 h-5 text-${config.color}-600 animate-pulse`} />
                <span className="text-base font-bold text-gray-800">Confidence Level</span>
              </div>
              <div className={`text-4xl font-black bg-gradient-to-r ${config.gradient} bg-clip-text text-transparent drop-shadow-sm`}>
                {(confidence * 100).toFixed(1)}%
              </div>
            </div>

            {/* Compact Progress Bar */}
            <div className="relative">
              <div className="w-full bg-gray-200/80 rounded-full h-4 shadow-inner overflow-hidden">
                <div
                  className={`h-4 bg-gradient-to-r ${config.gradient} rounded-full transition-all duration-[1500ms] ease-out shadow-lg relative overflow-hidden`}
                  style={{ width: `${confidence * 100}%` }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent animate-shimmer"></div>
                  <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Compact Analysis Cards */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 mb-2">
          <TrendingUp className="w-5 h-5 text-gray-700" />
          <h4 className="text-lg font-black text-gray-900">Detailed Analysis</h4>
        </div>
        
        {sortedProbs.map((item, index) => {
          const itemConfig = diseaseConfig[item.className] || diseaseConfig.healthy;
          const ItemIcon = itemConfig.icon;
          const isTopPrediction = index === 0;
          
          return (
            <div
              key={item.name}
              className={`relative bg-white rounded-xl p-4 shadow-md hover:shadow-lg transition-all duration-300 border ${
                isTopPrediction 
                  ? `${itemConfig.borderColor} border-2 ring-1 ring-${itemConfig.color}-200 ring-opacity-50` 
                  : 'border-gray-200'
              }`}
              style={{ 
                animationDelay: `${index * 100}ms`,
                animation: 'slideInUp 0.5s ease-out forwards'
              }}
            >
              {/* Compact Top Badge */}
              {isTopPrediction && (
                <div className={`absolute -top-2 -right-2 bg-gradient-to-r ${itemConfig.gradient} text-white px-3 py-0.5 rounded-full text-xs font-bold shadow-md flex items-center gap-1`}>
                  <Sparkles className="w-3 h-3" />
                  <span>Top</span>
                </div>
              )}

              <div className="flex items-center gap-3 mb-2">
                <div className={`bg-gradient-to-br ${itemConfig.gradient} p-2 rounded-lg shadow-md ${itemConfig.glowColor}`}>
                  <ItemIcon className="w-5 h-5 text-white drop-shadow" />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-center">
                    <span className="font-black text-gray-900 text-lg">{item.name}</span>
                    <span className={`text-xl font-black bg-gradient-to-r ${itemConfig.gradient} bg-clip-text text-transparent`}>
                      {(item.value * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
              
              {/* Compact Progress Bar */}
              <div className="relative">
                <div className="w-full bg-gray-100 rounded-full h-3 shadow-inner overflow-hidden">
                  <div
                    className={`h-3 bg-gradient-to-r ${itemConfig.gradient} rounded-full transition-all duration-[1200ms] ease-out relative overflow-hidden`}
                    style={{ 
                      width: `${item.value * 100}%`,
                      transitionDelay: `${index * 150}ms` 
                    }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent animate-shimmer"></div>
                    <div className="absolute inset-0 bg-white/30"></div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Compact Treatment Recommendations */}
      <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-2xl p-5 shadow-lg border border-blue-200">
        <div className="flex items-center gap-3 mb-3">
          <div className="bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 p-2 rounded-lg shadow-md">
            <Leaf className="w-5 h-5 text-white drop-shadow" />
          </div>
          <h4 className="text-lg font-black text-gray-900">Treatment Recommendations</h4>
        </div>
        <div className="grid gap-2">
          {config.recommendations.map((rec, index) => (
            <div
              key={index}
              className="flex items-start gap-3 bg-white/80 backdrop-blur-sm rounded-lg p-3 shadow-sm hover:shadow-md transition-all duration-200"
              style={{ 
                animationDelay: `${index * 100}ms`,
                animation: 'fadeIn 0.5s ease-out forwards'
              }}
            >
              <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-full p-1.5 flex-shrink-0 shadow-sm">
                <CheckCircle className="w-4 h-4 text-white" />
              </div>
              <span className="text-gray-800 font-semibold text-sm leading-relaxed">{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Compact Status Badge */}
      <div className="flex justify-center">
        {is_diseased ? (
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-full shadow-lg shadow-red-500/30 transform hover:scale-105 transition-transform">
            <AlertCircle className="w-5 h-5 animate-pulse" />
            <span className="font-black text-base">Disease Detected - Action Required</span>
          </div>
        ) : (
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-green-500 text-white rounded-full shadow-lg shadow-emerald-500/30 transform hover:scale-105 transition-transform">
            <CheckCircle className="w-5 h-5 animate-pulse" />
            <span className="font-black text-base">Healthy Leaf - Continue Monitoring</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionResult;
