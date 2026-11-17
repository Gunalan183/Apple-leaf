/**
 * Image Uploader Component
 * Beautiful drag & drop interface with enhanced animations
 */

import { useState, useCallback } from 'react';
import { Upload, Image as ImageIcon, X, Sparkles, Check } from 'lucide-react';

const ImageUploader = ({ onImageSelect, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (JPEG, PNG)');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);

    // Pass file to parent
    onImageSelect(file);
  };

  const clearImage = () => {
    setPreview(null);
    onImageSelect(null);
  };

  return (
    <div className="w-full">
      {!preview ? (
        <div
          className={`
            relative border-3 border-dashed rounded-3xl p-12 text-center
            transition-all duration-300 transform
            ${dragActive 
              ? 'border-emerald-500 bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 scale-[1.02] shadow-2xl shadow-emerald-500/20' 
              : 'border-gray-300 bg-gradient-to-br from-white to-gray-50 hover:border-emerald-400 hover:shadow-xl'
            }
            ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:-translate-y-1'}
          `}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {/* Decorative Background Pattern */}
          <div className="absolute inset-0 opacity-5 rounded-3xl overflow-hidden">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0)',
              backgroundSize: '24px 24px'
            }}></div>
          </div>

          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept="image/*"
            onChange={handleChange}
            disabled={isLoading}
          />
          
          <label
            htmlFor="file-upload"
            className="relative cursor-pointer flex flex-col items-center"
          >
            {/* Animated Upload Icon */}
            <div className={`
              relative mb-6 p-6 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-xl
              transform transition-all duration-300
              ${dragActive ? 'scale-110 rotate-6' : 'hover:scale-105'}
            `}>
              <Upload className={`w-16 h-16 text-white drop-shadow-lg ${dragActive ? 'animate-bounce' : ''}`} />
              {dragActive && (
                <div className="absolute -top-2 -right-2">
                  <Sparkles className="w-8 h-8 text-yellow-400 animate-pulse" />
                </div>
              )}
            </div>

            {/* Main Text */}
            <p className="text-3xl font-black text-gray-900 mb-3 bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              {dragActive ? '✨ Drop it here!' : 'Upload Leaf Image'}
            </p>
            
            <p className="text-lg text-gray-600 font-semibold mb-6">
              {dragActive ? 'Release to upload' : 'Drag and drop or click to browse'}
            </p>

            {/* Feature Pills */}
            <div className="flex flex-wrap gap-3 justify-center mb-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md border border-gray-200">
                <ImageIcon className="w-4 h-4 text-emerald-600" />
                <span className="text-sm font-semibold text-gray-700">JPEG, PNG</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md border border-gray-200">
                <Check className="w-4 h-4 text-emerald-600" />
                <span className="text-sm font-semibold text-gray-700">Max 10MB</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md border border-gray-200">
                <Sparkles className="w-4 h-4 text-emerald-600" />
                <span className="text-sm font-semibold text-gray-700">AI Powered</span>
              </div>
            </div>

            <p className="text-xs text-gray-400 font-medium">
              Fast and accurate disease detection in seconds
            </p>
          </label>
        </div>
      ) : (
        <div className="relative animate-fadeIn">
          {/* Preview Card */}
          <div className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200 shadow-2xl border-2 border-gray-300">
            {/* Image Container */}
            <div className="relative">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-auto max-h-[500px] object-contain"
              />
              
              {/* Overlay Gradient */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent pointer-events-none"></div>

              {/* Remove Button */}
              {!isLoading && (
                <button
                  onClick={clearImage}
                  className="absolute top-4 right-4 p-3 bg-gradient-to-br from-red-500 to-rose-600 text-white rounded-full hover:from-red-600 hover:to-rose-700 transition-all duration-200 shadow-xl hover:shadow-2xl transform hover:scale-110"
                  title="Remove image"
                >
                  <X className="w-6 h-6" />
                </button>
              )}

              {/* Loading Overlay */}
              {isLoading && (
                <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center">
                  <div className="text-center">
                    <div className="relative inline-block">
                      <div className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <Sparkles className="w-8 h-8 text-white absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse" />
                    </div>
                    <p className="text-white font-bold text-xl mt-4">Analyzing leaf...</p>
                    <p className="text-white/80 text-sm mt-2">AI is working its magic ✨</p>
                  </div>
                </div>
              )}
            </div>

            {/* Status Bar */}
            <div className={`px-6 py-4 ${isLoading ? 'bg-gradient-to-r from-blue-500 to-indigo-500' : 'bg-gradient-to-r from-emerald-500 to-teal-500'}`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {isLoading ? (
                    <>
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                      <span className="text-white font-bold text-lg">Processing...</span>
                    </>
                  ) : (
                    <>
                      <Check className="w-6 h-6 text-white" />
                      <span className="text-white font-bold text-lg">Ready for Analysis</span>
                    </>
                  )}
                </div>
                {!isLoading && (
                  <button
                    onClick={clearImage}
                    className="text-white hover:text-white/80 font-semibold text-sm underline transition-colors"
                  >
                    Change Image
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Info Card */}
          {!isLoading && (
            <div className="mt-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-4 border-2 border-blue-200 shadow-lg">
              <p className="text-center text-gray-700 font-semibold flex items-center justify-center gap-2">
                <Sparkles className="w-5 h-5 text-blue-600" />
                <span>Click analyze button below to detect diseases</span>
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
