import React from "react";
import { Stethoscope, CheckCircle2, XCircle } from "lucide-react";

interface ClinicalFindingsProps {
  findings: string[];
}

const ClinicalFindings: React.FC<ClinicalFindingsProps> = ({ findings }) => {
  if (!findings || findings.length === 0) return null;

  // We parse the free-text findings returned by the API into structured medical cards
  // based on keyword matching, as requested by the user.
  const structuredData = [
    { name: "Microaneurysms", keyword: "microaneurysm" },
    { name: "Hard Exudates", keyword: "hard exudate" },
    { name: "Cotton Wool Spots", keyword: "cotton wool" },
    { name: "Hemorrhages", keyword: "hemorrhage" },
    { name: "Neovascularization", keyword: "neovascularization" },
    { name: "Intraretinal Microvascular Abnormalities", keyword: "irma" },
  ];

  const findingsText = findings.join(" ").toLowerCase();

  return (
    <div className="premium-card mb-6">
      <div className="premium-card-header">
        <div className="flex items-center gap-2">
          <Stethoscope className="w-5 h-5 text-blue-600" />
          <span>Structured Clinical Findings</span>
        </div>
      </div>
      
      <div className="premium-card-body">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
          {structuredData.map((item, idx) => {
            const isDetected = findingsText.includes(item.keyword);
            return (
              <div key={idx} className="border border-gray-200 rounded p-3 flex flex-col justify-between h-full bg-gray-50">
                <span className="text-xs font-bold text-gray-700 leading-tight mb-2">{item.name}</span>
                <div className="flex items-center gap-1.5 mt-auto">
                  {isDetected ? (
                    <>
                      <CheckCircle2 className="w-4 h-4 text-orange-500" />
                      <span className="text-[10px] uppercase font-bold text-orange-600">Detected</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-4 h-4 text-green-500" />
                      <span className="text-[10px] uppercase font-bold text-green-600">Not Detected</span>
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs font-bold text-gray-500 uppercase mb-2">Automated Notes</p>
          <ul className="space-y-1.5">
            {findings.map((f, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span> {f}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ClinicalFindings;
