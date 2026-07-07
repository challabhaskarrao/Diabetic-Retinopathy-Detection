import React, { useState } from "react";
import { Maximize, ZoomIn, Download, Eye, Info } from "lucide-react";

interface GradCamViewerProps {
  originalImage: string | null;
  heatmapImage: string | null;
}

const GradCamViewer: React.FC<GradCamViewerProps> = ({ originalImage, heatmapImage }) => {
  const [isZoomed, setIsZoomed] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  if (!originalImage || !heatmapImage) return null;

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const handleDownload = () => {
    const a = document.createElement("a");
    a.href = heatmapImage;
    a.download = "GradCAM_Overlay.jpg";
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  const FullscreenModal = () => (
    <div className="fixed inset-0 z-[100] bg-black bg-opacity-95 flex items-center justify-center p-4">
      <button 
        onClick={toggleFullscreen}
        className="absolute top-6 right-6 text-white hover:text-gray-300"
      >
        Close (Esc)
      </button>
      <div className="max-w-6xl w-full h-full flex flex-col items-center justify-center gap-4">
        <h3 className="text-white text-lg font-semibold">Grad-CAM Explainability Map</h3>
        <img 
          src={heatmapImage} 
          alt="Grad-CAM Fullscreen" 
          className="max-h-[85vh] max-w-full object-contain border border-gray-700"
        />
      </div>
    </div>
  );

  return (
    <>
      <div className="premium-card mb-6">
        <div className="premium-card-header">
          <div className="flex items-center gap-2">
            <Eye className="w-5 h-5 text-blue-600" />
            <span>AI Interpretability (Grad-CAM)</span>
          </div>
          <div className="flex gap-2">
            <button onClick={() => setIsZoomed(!isZoomed)} className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded" title="Zoom">
              <ZoomIn className="w-4 h-4" />
            </button>
            <button onClick={toggleFullscreen} className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded" title="Fullscreen">
              <Maximize className="w-4 h-4" />
            </button>
            <button onClick={handleDownload} className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded" title="Download">
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="premium-card-body">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs font-bold text-gray-500 uppercase mb-2 text-center">Original Input</p>
              <div className="bg-black rounded-lg overflow-hidden border border-gray-200 aspect-square flex items-center justify-center">
                <img src={originalImage} alt="Original" className="w-full h-full object-contain" />
              </div>
            </div>
            <div>
              <p className="text-xs font-bold text-blue-600 uppercase mb-2 text-center">Grad-CAM Overlay</p>
              <div className={`bg-black rounded-lg overflow-hidden border border-blue-200 aspect-square flex items-center justify-center transition-transform duration-300 ${isZoomed ? 'scale-110 shadow-xl z-10 relative' : ''}`}>
                <img src={heatmapImage} alt="Heatmap" className="w-full h-full object-contain" />
              </div>
            </div>
          </div>
          
          <div className="mt-4 p-3 bg-blue-50 rounded text-xs text-blue-800 border border-blue-100 flex gap-2">
            <Info className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <p>Red/Yellow regions indicate areas of high network activation. These are the primary lesions or structures the AI used to determine the severity grade.</p>
          </div>
        </div>
      </div>
      
      {isFullscreen && <FullscreenModal />}
    </>
  );
};

export default GradCamViewer;
