import React from "react";
import { BarChart3 } from "lucide-react";

interface ProbabilityDistributionProps {
  probabilities: number[];
}

const ProbabilityDistribution: React.FC<ProbabilityDistributionProps> = ({ probabilities }) => {
  if (!probabilities || probabilities.length === 0) return null;

  const classes = [
    { name: "No DR", color: "bg-green-500" },
    { name: "Mild", color: "bg-yellow-400" },
    { name: "Moderate", color: "bg-amber-500" },
    { name: "Severe", color: "bg-orange-500" },
    { name: "Proliferative", color: "bg-red-600" }
  ];

  return (
    <div className="premium-card mb-6">
      <div className="premium-card-header">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-600" />
          <span>Probability Distribution</span>
        </div>
      </div>
      
      <div className="premium-card-body">
        <div className="space-y-4">
          {classes.map((cls, idx) => {
            const prob = probabilities[idx] || 0;
            const percentage = (prob * 100).toFixed(1);
            
            return (
              <div key={idx}>
                <div className="flex justify-between text-xs font-semibold mb-1 text-gray-700">
                  <span>{cls.name}</span>
                  <span>{percentage}%</span>
                </div>
                <div className="progress-bg">
                  <div 
                    className={`progress-fill ${cls.color}`} 
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ProbabilityDistribution;
