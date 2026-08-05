import React from "react";
import { Download, Printer, Database } from "lucide-react";

interface ReportPreviewProps {
  onPrint: () => void;
}

const ReportPreview: React.FC<ReportPreviewProps> = ({ onPrint }) => {
  return (
    <div className="mt-8 mb-6 flex flex-wrap items-center gap-3 no-print">
      <button
        type="button"
        onClick={onPrint}
        className="btn-primary"
      >
        <Printer className="w-4 h-4" aria-hidden="true" />
        Print Report
      </button>

      <button
        type="button"
        onClick={onPrint}
        className="btn-secondary"
      >
        <Download className="w-4 h-4" aria-hidden="true" />
        Download PDF
      </button>

      <div className="ml-auto relative group">
        <button
          type="button"
          disabled
          className="btn-secondary"
        >
          <Database className="w-4 h-4" aria-hidden="true" />
          Save to Database
        </button>
        <div className="absolute bottom-full right-0 mb-2 w-48 p-2 bg-slate-800 text-white text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-10 text-center">
          Database integration not configured in local environment.
        </div>
      </div>
    </div>
  );
};

export default ReportPreview;
