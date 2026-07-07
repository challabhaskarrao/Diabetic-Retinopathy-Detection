import React from "react";
import { Server, Database, Code2 } from "lucide-react";

const SidebarStats: React.FC = () => {
  return (
    <div className="premium-card bg-slate-50 border-slate-200 no-print">
      <div className="premium-card-header bg-transparent border-b border-slate-200 pb-3">
        <h3 className="text-sm font-bold text-slate-800">Model Specifications</h3>
      </div>
      <div className="premium-card-body p-4 space-y-4">
        
        <div className="flex items-start gap-3">
          <div className="p-2 bg-white rounded shadow-sm border border-slate-100 text-blue-600">
            <Server className="w-4 h-4" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-slate-500 uppercase">Architecture</p>
            <p className="text-xs font-semibold text-slate-900">EfficientNet-B3 (PyTorch)</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Transfer Learning + Fine-tuning</p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="p-2 bg-white rounded shadow-sm border border-slate-100 text-blue-600">
            <Database className="w-4 h-4" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-slate-500 uppercase">Training Datasets</p>
            <p className="text-xs font-semibold text-slate-900">APTOS, EyePACS, IDRiD</p>
            <p className="text-[10px] text-slate-500 mt-0.5">&gt; 50,000 retinal images</p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="p-2 bg-white rounded shadow-sm border border-slate-100 text-blue-600">
            <Code2 className="w-4 h-4" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-slate-500 uppercase">Model Accuracy</p>
            <p className="text-xs font-semibold text-slate-900">94.2% (Validation)</p>
            <p className="text-[10px] text-slate-500 mt-0.5">AUC: 0.98, Kappa: 0.89</p>
          </div>
        </div>
        
        <div className="pt-3 border-t border-slate-200">
          <p className="text-[10px] text-slate-400 text-center">Last Updated: Oct 2023</p>
        </div>
      </div>
    </div>
  );
};

export default SidebarStats;
