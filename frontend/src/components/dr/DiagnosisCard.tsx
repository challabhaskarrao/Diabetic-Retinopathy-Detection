import React from "react";
import { Activity, Clock, Cpu } from "lucide-react";
import { DRDetails } from "../../types";

interface DiagnosisCardProps {
  report: DRDetails;
  processingTime?: number;
}

const DiagnosisCard: React.FC<DiagnosisCardProps> = ({ report, processingTime }) => {
  // Severity grading mapping
  const getSeverityBadge = (level: number) => {
    switch (level) {
      case 0: return { label: "No DR", class: "badge-success" };
      case 1: return { label: "Mild NPDR", class: "badge-warning" };
      case 2: return { label: "Moderate NPDR", class: "badge-warning" };
      case 3: return { label: "Severe NPDR", class: "badge-critical" };
      case 4: return { label: "Proliferative DR", class: "badge-critical" };
      default: return { label: "Unknown", class: "badge-neutral" };
    }
  };

  const badge = getSeverityBadge(report.severityLevel);

  return (
    <div className="premium-card mb-6 border-t-4 border-blue-600">
      <div className="premium-card-body">
        
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-1">Diagnostic Assessment</h2>
            <p className="text-sm text-gray-500">AI-generated preliminary screening report</p>
          </div>
          
          <div className="mt-4 md:mt-0 flex items-center gap-2 bg-gray-50 px-4 py-2 rounded-lg border border-gray-200">
            <span className="text-xs font-bold text-gray-500 uppercase">Confidence</span>
            <span className="text-lg font-black text-blue-600">
              {(report.confidence * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
          
          <div className="bg-white border border-gray-200 rounded-lg p-4 text-center shadow-sm">
            <p className="text-xs uppercase font-bold text-gray-500 mb-2">Predicted Grade</p>
            <div className="flex justify-center items-center gap-2">
              <span className="text-3xl font-black text-gray-900">{report.severityLevel}</span>
              <span className="text-lg font-bold text-gray-400">/ 4</span>
            </div>
            <p className="text-xs text-gray-500 mt-1">{report.status}</p>
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-4 text-center shadow-sm flex flex-col items-center justify-center">
            <p className="text-xs uppercase font-bold text-gray-500 mb-3">Risk Level</p>
            <span className={`badge text-sm px-3 py-1 ${badge.class}`}>
              {badge.label}
            </span>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4 text-left shadow-sm flex flex-col justify-center space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-gray-500">
                <Clock className="w-4 h-4" />
                <span className="text-xs font-bold uppercase">Processing Time</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">{processingTime ? processingTime.toFixed(2) : "1.24"} s</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-gray-500">
                <Cpu className="w-4 h-4" />
                <span className="text-xs font-bold uppercase">Inference Device</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">CUDA / GPU</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-gray-500">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-bold uppercase">Model Version</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">EN-B3-DR-v1.0</span>
            </div>
          </div>

        </div>
        
      </div>
    </div>
  );
};

export default DiagnosisCard;
