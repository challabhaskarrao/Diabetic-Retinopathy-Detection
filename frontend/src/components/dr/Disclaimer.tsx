import React from "react";
import { AlertTriangle } from "lucide-react";

const Disclaimer: React.FC = () => {
  return (
    <div className="mt-12 mb-8 p-4 rounded-lg bg-amber-50 border border-amber-200 flex gap-3 text-amber-800 max-w-4xl mx-auto no-print">
      <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-600" aria-hidden="true" />
      <div>
        <h4 className="text-sm font-bold mb-1">Important Medical Disclaimer</h4>
        <p className="text-xs leading-relaxed">
          This AI system is intended for screening and decision-support purposes only. It is not a substitute for professional medical judgment. 
          Final diagnosis and treatment planning must be confirmed by a qualified ophthalmologist or retinal specialist. 
          The confidence scores and predictive models are based on statistical probabilities and may not account for all clinical variables.
        </p>
      </div>
    </div>
  );
};

export default Disclaimer;
