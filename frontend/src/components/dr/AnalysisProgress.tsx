import React from "react";
import { Loader2, PlayCircle } from "lucide-react";

interface AnalysisProgressProps {
  isReady: boolean;
  isAnalyzing: boolean;
  loadingText: string;
  onClick: () => void;
}

const AnalysisProgress: React.FC<AnalysisProgressProps> = ({
  isReady,
  isAnalyzing,
  loadingText,
  onClick
}) => {
  return (
    <div className="premium-card mb-6">
      <div className="premium-card-body p-6 text-center">
        
        {!isAnalyzing ? (
          <div>
            <button
              type="button"
              onClick={onClick}
              disabled={!isReady}
              className="btn-primary text-base py-3 px-8 w-full md:w-auto"
            >
              <PlayCircle className="w-5 h-5" />
              Analyze Retinal Image
            </button>
            {!isReady && (
              <p className="text-xs text-amber-600 mt-3 font-medium">
                Please complete patient form and upload an image to enable analysis.
              </p>
            )}
          </div>
        ) : (
          <div className="py-4">
            <Loader2 className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
            <h3 className="text-sm font-bold text-gray-900 mb-1">Processing Analysis</h3>
            <p className="text-xs text-blue-600 font-semibold animate-pulse">{loadingText}</p>
            
            {/* Fake progress steps for visual feedback */}
            <div className="flex justify-center gap-2 mt-4">
              <div className={`w-2 h-2 rounded-full ${loadingText.includes('Uploading') ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
              <div className={`w-2 h-2 rounded-full ${loadingText.includes('Assessing') ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
              <div className={`w-2 h-2 rounded-full ${loadingText.includes('inference') ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
              <div className={`w-2 h-2 rounded-full ${loadingText.includes('map') ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
};

export default AnalysisProgress;
