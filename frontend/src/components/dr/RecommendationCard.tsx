import React from "react";
import { ClipboardList, Calendar, UserPlus } from "lucide-react";

interface RecommendationCardProps {
  severityLevel: number;
  recommendations: string[];
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ severityLevel, recommendations }) => {
  if (recommendations.length === 0) return null;

  // Determine structured blocks based on severity
  let interval = "12 Months";
  let referral = "Primary Care";
  let risk = "Low";
  
  if (severityLevel === 1) {
    interval = "6-12 Months";
    referral = "Optometrist / Primary Care";
    risk = "Mild";
  } else if (severityLevel === 2) {
    interval = "2-3 Months";
    referral = "Ophthalmologist";
    risk = "Moderate";
  } else if (severityLevel === 3) {
    interval = "2-4 Weeks";
    referral = "Retina Specialist";
    risk = "High";
  } else if (severityLevel === 4) {
    interval = "Immediate";
    referral = "Urgent Retina Specialist";
    risk = "Critical";
  }

  // Calculate next screening date for UI
  const nextDate = new Date();
  if (severityLevel === 0) nextDate.setFullYear(nextDate.getFullYear() + 1);
  else if (severityLevel === 1) nextDate.setMonth(nextDate.getMonth() + 6);
  else if (severityLevel === 2) nextDate.setMonth(nextDate.getMonth() + 3);
  else if (severityLevel === 3) nextDate.setDate(nextDate.getDate() + 21);
  
  const formattedNextDate = severityLevel === 4 ? "ASAP" : nextDate.toLocaleDateString();

  return (
    <div className="premium-card mb-6">
      <div className="premium-card-header bg-blue-50 border-blue-100 text-blue-900">
        <div className="flex items-center gap-2">
          <ClipboardList className="w-5 h-5 text-blue-600" />
          <span>Clinical Recommendations</span>
        </div>
      </div>
      
      <div className="premium-card-body">
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Risk Assessment</p>
            <p className="text-sm font-bold text-gray-900">{risk}</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Follow-up Interval</p>
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-blue-500" />
              <p className="text-sm font-bold text-gray-900">{interval}</p>
            </div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Referral</p>
            <div className="flex items-center gap-1.5">
              <UserPlus className="w-3.5 h-3.5 text-blue-500" />
              <p className="text-sm font-bold text-gray-900 truncate" title={referral}>{referral}</p>
            </div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-[10px] uppercase font-bold text-gray-500 mb-1">Next Screening</p>
            <p className="text-sm font-bold text-gray-900">{formattedNextDate}</p>
          </div>
        </div>

        <div>
          <p className="text-xs font-bold text-gray-500 uppercase mb-2">Detailed Plan</p>
          <ul className="space-y-2">
            {recommendations.map((rec, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2 bg-gray-50 p-2 rounded border border-gray-100">
                <span className="text-blue-500 mt-0.5 font-bold">{i+1}.</span> {rec}
              </li>
            ))}
          </ul>
        </div>
        
      </div>
    </div>
  );
};

export default RecommendationCard;
