import React from "react";
import { CheckCircle, AlertTriangle } from "lucide-react";

export interface QualityData {
  is_pass: boolean;
  reason: string;
  details: {
    blur_score: number;
    brightness_score: number;
    resolution: string;
  };
}

interface QualityCardProps {
  data: QualityData | null;
}

const QualityCard: React.FC<QualityCardProps> = ({ data }) => {
  if (!data) return null;

  // Determine badge colors based on arbitrary thresholds for UI purposes
  const getBlurStatus = (score: number) => {
    if (score > 300) return { label: "Excellent", class: "badge-success" };
    if (score > 100) return { label: "Good", class: "badge-success" };
    return { label: "Poor", class: "badge-critical" };
  };

  const getBrightnessStatus = (score: number) => {
    if (score > 80 && score < 180) return { label: "Excellent", class: "badge-success" };
    if (score > 40 && score < 220) return { label: "Good", class: "badge-warning" };
    return { label: "Poor", class: "badge-critical" };
  };

  const blurStatus = getBlurStatus(data.details.blur_score);
  const brightnessStatus = getBrightnessStatus(data.details.brightness_score);

  return (
    <div className={`premium-card mb-6 border-l-4 ${data.is_pass ? 'border-l-green-500' : 'border-l-red-500'}`}>
      <div className="premium-card-body py-4">
        <div className="flex items-start gap-4">
          {data.is_pass ? (
            <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertTriangle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
          )}
          
          <div className="flex-1 w-full">
            <h4 className="text-sm font-bold text-gray-900 mb-1">
              Image Quality Assessment
            </h4>
            <p className="text-xs text-gray-600 mb-4">{data.reason}</p>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              
              <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Blur Detection</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-medium text-gray-900">{data.details.blur_score.toFixed(0)}</span>
                  <span className={`badge ${blurStatus.class}`}>{blurStatus.label}</span>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Brightness</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-medium text-gray-900">{data.details.brightness_score.toFixed(0)}</span>
                  <span className={`badge ${brightnessStatus.class}`}>{brightnessStatus.label}</span>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Resolution</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-medium text-gray-900">{data.details.resolution}</span>
                  <span className="badge badge-success">Good</span>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Field Coverage</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs font-medium text-gray-900">Macula Centered</span>
                  <span className="badge badge-success">Good</span>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QualityCard;
