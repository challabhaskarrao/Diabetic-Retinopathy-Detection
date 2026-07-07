import React from "react";
import { Zap, Loader2 } from "lucide-react";

interface AnalysisButtonProps {
  isReady: boolean;
  isAnalyzing: boolean;
  onClick: () => void;
}

const AnalysisButton: React.FC<AnalysisButtonProps> = ({
  isReady,
  isAnalyzing,
  onClick,
}) => {
  return (
    <div className="flex justify-center my-8 no-print">
      <button
        type="button"
        onClick={onClick}
        disabled={!isReady || isAnalyzing}
        className={`relative flex items-center justify-center gap-2.5 w-full max-w-sm py-4 px-6 rounded-xl text-base font-bold text-white transition-all overflow-hidden ${
          !isReady
            ? "bg-slate-300 cursor-not-allowed shadow-none"
            : isAnalyzing
            ? "bg-blue-600 cursor-wait shadow-lg shadow-blue-600/30"
            : "bg-blue-600 hover:bg-blue-700 active:scale-[0.98] cursor-pointer shadow-lg shadow-blue-600/30 hover:shadow-xl hover:shadow-blue-600/40"
        }`}
        aria-disabled={!isReady || isAnalyzing}
        aria-busy={isAnalyzing}
      >
        {isAnalyzing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
            <span>Running AI Analysis...</span>
            
            {/* Indeterminate loading bar at bottom */}
            <div className="absolute bottom-0 left-0 h-1 w-full bg-blue-700/50">
              <div 
                className="h-full bg-white/40 animate-[progress_1.5s_ease-in-out_infinite] w-1/3 rounded-full" 
                style={{
                  animationName: 'progress-indeterminate',
                  animationDuration: '1.5s',
                  animationTimingFunction: 'ease-in-out',
                  animationIterationCount: 'infinite'
                }}
              />
            </div>
            
            {/* Inject keyframes just for this button if needed, though Tailwind might need a custom class.
                We'll add a simple style block for the indeterminate animation. */}
            <style>{`
              @keyframes progress-indeterminate {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
                100% { transform: translateX(300%); }
              }
            `}</style>
          </>
        ) : (
          <>
            <Zap className="w-5 h-5" aria-hidden="true" />
            <span>Analyze Retinal Image</span>
          </>
        )}
      </button>
    </div>
  );
};

export default AnalysisButton;
