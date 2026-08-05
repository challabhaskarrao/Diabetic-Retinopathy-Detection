import React, { useState, useEffect, useCallback } from "react";
import {
  Shield, Upload, RotateCcw, Trash2, CheckCircle2, XCircle,
  AlertTriangle, Clock, Cpu, BarChart3, Microscope, Stethoscope,
  FileText, Download, Printer, Code2, ZoomIn, Maximize, Info,
  Zap, Loader2, UserRound, ClipboardList, ChevronRight,
  Activity, Calendar, TrendingUp, ScanLine, Eye
} from "lucide-react";

/* ─── Types ─────────────────────────────────────────────────── */
interface PatientData {
  patientId: string; patientName: string; age: string; gender: string;
  eye: string; diabetesDuration: string; hba1c: string;
  referringDoctor: string; hospital: string; examinationDate: string;
}
interface QualityResult {
  is_pass: boolean; reason: string;
  details: { blur_score: number; brightness_score: number; resolution: string };
}
interface PredictionResult {
  prediction: string; grade: number; confidence: number;
  probabilities: number[]; processing_time: number;
  findings: string[]; recommendations: string[];
}

/* ─── Panel wrapper ──────────────────────────────────────────── */
const Panel: React.FC<{
  iconColor?: string; title: string; icon: React.ReactNode;
  children: React.ReactNode; className?: string;
}> = ({ iconColor = "#3B82F6", title, icon, children, className = "" }) => (
  <div className={`panel ${className}`}>
    <div className="panel-head">
      <span style={{ color: iconColor }} className="flex-shrink-0">{icon}</span>
      <span className="panel-title">{title}</span>
    </div>
    <div className="panel-body">{children}</div>
  </div>
);

/* ═══════════════════════════════════════════════════════════════
   ROW 1: Patient Info + Image Upload
═══════════════════════════════════════════════════════════════ */
const PatientPanel: React.FC<{ data: PatientData; onChange: (d: PatientData) => void }> = ({ data, onChange }) => {
  const set = (k: keyof PatientData) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => onChange({ ...data, [k]: e.target.value });

  return (
    <Panel iconColor="#6366F1" title="Patient Information" icon={<UserRound className="w-4 h-4" />}>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-5">
        <div className="sm:col-span-1 lg:col-span-1">
          <label className="f-label">Patient ID *</label>
          <input className="f-input" value={data.patientId} onChange={set("patientId")} placeholder="MRN-00000" />
        </div>
        <div className="sm:col-span-2 lg:col-span-2">
          <label className="f-label">Full Name *</label>
          <input className="f-input" value={data.patientName} onChange={set("patientName")} placeholder="Patient full name" />
        </div>
        <div>
          <label className="f-label">Age (yrs) *</label>
          <input type="number" className="f-input" value={data.age} onChange={set("age")} placeholder="e.g. 52" />
        </div>
        <div>
          <label className="f-label">Gender *</label>
          <select className="f-input" value={data.gender} onChange={set("gender")}>
            <option value="" disabled>Select</option>
            <option>Male</option><option>Female</option><option>Other</option>
          </select>
        </div>
        <div>
          <label className="f-label">Eye Examined *</label>
          <select className="f-input" value={data.eye} onChange={set("eye")}>
            <option value="" disabled>Select</option>
            <option value="OD">Right (OD)</option>
            <option value="OS">Left (OS)</option>
            <option value="OU">Both (OU)</option>
          </select>
        </div>
        <div>
          <label className="f-label">Visit Date *</label>
          <input type="date" className="f-input" value={data.examinationDate} onChange={set("examinationDate")} />
        </div>
        <div>
          <label className="f-label">DM Duration (yrs)</label>
          <input type="number" className="f-input" value={data.diabetesDuration} onChange={set("diabetesDuration")} placeholder="e.g. 5" />
        </div>
        <div>
          <label className="f-label">HbA1c (%)</label>
          <input type="number" step="0.1" className="f-input" value={data.hba1c} onChange={set("hba1c")} placeholder="e.g. 7.5" />
        </div>
        <div>
          <label className="f-label">Referring Doctor</label>
          <input className="f-input" value={data.referringDoctor} onChange={set("referringDoctor")} placeholder="Dr. Name" />
        </div>
        <div>
          <label className="f-label">Hospital / Clinic</label>
          <input className="f-input" value={data.hospital} onChange={set("hospital")} placeholder="Facility name" />
        </div>
      </div>
    </Panel>
  );
};

const ImagePanel: React.FC<{
  file: File | null; preview: string | null;
  onChange: (f: File | null, p: string | null, b: string | null) => void;
}> = ({ file, preview, onChange }) => {
  const process = useCallback((f: File) => {
    if (!f.type.startsWith("image/")) { alert("Please upload a valid image."); return; }
    if (f.size > 10 * 1024 * 1024) { alert("File exceeds 10 MB."); return; }
    const url = URL.createObjectURL(f);
    const reader = new FileReader();
    reader.onload = () => onChange(f, url, reader.result as string);
    reader.readAsDataURL(f);
  }, [onChange]);

  return (
    <Panel iconColor="#8B5CF6" title="Retinal Image Upload" icon={<Upload className="w-4 h-4" />}>
      {!preview ? (
        <div
          className="drop-zone flex flex-col items-center justify-center py-12 px-6 text-center"
          onDragOver={e => { e.preventDefault(); e.currentTarget.classList.add("over"); }}
          onDragLeave={e => e.currentTarget.classList.remove("over")}
          onDrop={e => { e.preventDefault(); e.currentTarget.classList.remove("over"); if (e.dataTransfer.files[0]) process(e.dataTransfer.files[0]); }}
          onClick={() => document.getElementById("img-input")?.click()}
        >
          <input id="img-input" type="file" className="hidden" accept="image/jpeg,image/png"
            onChange={e => { if (e.target.files?.[0]) process(e.target.files[0]); }} />
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5 shadow-sm"
            style={{ background: "rgba(139, 92, 246, 0.1)", border: "1px solid rgba(139, 92, 246, 0.2)" }}>
            <Upload className="w-7 h-7 text-violet-500" />
          </div>
          <p className="text-sm font-bold text-slate-700 mb-2">Drag & drop retinal fundus image</p>
          <p className="text-xs text-slate-500 mb-5">or click to browse</p>
          <div className="flex gap-3">
            {["JPEG", "PNG", "Max 10 MB"].map(t => (
              <span key={t} className="text-[10.5px] font-semibold bg-slate-100 text-slate-500 px-3 py-1 rounded-full">{t}</span>
            ))}
          </div>
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row gap-6 items-start">
          <div className="w-full sm:w-64 h-56 flex-shrink-0 bg-slate-900 rounded-2xl overflow-hidden border border-slate-200 flex items-center justify-center relative group shadow-sm">
            <img src={preview} alt="Retinal scan" className="max-w-full max-h-full object-contain" />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-center pb-4">
              <ScanLine className="w-6 h-6 text-white animate-pulse" />
            </div>
          </div>
          <div className="flex-1 w-full">
            <div className="inline-flex items-center gap-1.5 bg-emerald-50 border border-emerald-200 rounded-full px-3 py-1.5 mb-4">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span className="text-[11px] font-bold text-emerald-700 tracking-wide uppercase">Image Loaded</span>
            </div>
            <p className="text-lg font-bold text-slate-900 break-all mb-1">{file?.name}</p>
            <p className="text-xs text-slate-500 mb-1 font-medium">{file?.type}</p>
            <p className="text-xs text-slate-500 mb-6">{file ? (file.size / 1048576).toFixed(2) : 0} MB</p>
            <div className="flex flex-wrap gap-3">
              <button className="btn-sm btn-sm-white" onClick={() => document.getElementById("img-retake")?.click()}>
                <RotateCcw className="w-3.5 h-3.5" /> Retake Image
              </button>
              <input id="img-retake" type="file" className="hidden" accept="image/jpeg,image/png"
                onChange={e => { if (e.target.files?.[0]) process(e.target.files[0]); }} />
              <button className="btn-sm btn-sm-ghost" onClick={() => onChange(null, null, null)}>
                <Trash2 className="w-3.5 h-3.5" /> Remove
              </button>
            </div>
          </div>
        </div>
      )}
    </Panel>
  );
};

/* ═══════════════════════════════════════════════════════════════
   ANALYZE BUTTON + LOADING
═══════════════════════════════════════════════════════════════ */
const AnalyzeSection: React.FC<{
  isReady: boolean; isAnalyzing: boolean; loadingText: string; onAnalyze: () => void;
}> = ({ isReady, isAnalyzing, loadingText, onAnalyze }) => (
  <div className="panel">
    <div className="panel-body">
      {!isAnalyzing ? (
        <div className="flex flex-col sm:flex-row items-center gap-5">
          <button className="btn-analyze sm:w-auto px-12" onClick={onAnalyze} disabled={!isReady}>
            <Zap className="w-5 h-5" /> Initialize AI Analysis
          </button>
          {!isReady && (
            <div className="flex items-center gap-2 px-4 py-2 bg-amber-50 border border-amber-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <p className="text-xs text-amber-700 font-medium">Complete required fields (*) and upload an image.</p>
            </div>
          )}
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row sm:items-center gap-5">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center relative shadow-sm">
            <div className="absolute inset-0 rounded-full border-t-2 border-blue-500 animate-spin" />
            <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />
          </div>
          <div>
            <p className="text-base font-bold text-slate-800 tracking-wide">Processing Retinal Image…</p>
            <p className="text-sm text-blue-600 animate-pulse mt-0.5">{loadingText}</p>
          </div>
          <div className="sm:ml-auto flex gap-3 items-center">
            {["Upload", "Quality", "Inference", "Grad-CAM"].map((step) => (
              <div key={step} className="flex flex-col items-center gap-1.5">
                <div className={`w-2 h-2 rounded-full transition-colors ${
                  loadingText.toLowerCase().includes(step.toLowerCase().slice(0, 5))
                    ? "bg-blue-500 shadow-md" : "bg-slate-200"
                }`} />
                <span className="text-[10px] font-medium text-slate-400 hidden lg:block uppercase tracking-wider">{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  </div>
);

/* ═══════════════════════════════════════════════════════════════
   RESULTS — shown only after analysis
═══════════════════════════════════════════════════════════════ */

/* Quality */
const QualityPanel: React.FC<{ data: QualityResult }> = ({ data }) => {
  const blurBadge   = (s: number): [string, string] => s > 300 ? ["Excellent", "tag-green"] : s > 100 ? ["Good", "tag-green"] : ["Poor", "tag-red"];
  const brightBadge = (s: number): [string, string] => (s > 60 && s < 190) ? ["Excellent", "tag-green"] : (s > 35 && s < 220) ? ["Good", "tag-amber"] : ["Poor", "tag-red"];

  return (
    <Panel iconColor="#14B8A6" title="Image Quality Assessment" icon={<Shield className="w-4 h-4" />}>
      <div className={`flex items-start gap-3 p-4 rounded-xl mb-5 glass-card ${data.is_pass ? "bg-emerald-50 border-emerald-200" : "bg-red-50 border-red-200"}`}>
        {data.is_pass
          ? <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0" />
          : <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />}
        <p className={`text-sm font-semibold leading-relaxed ${data.is_pass ? "text-emerald-800" : "text-red-800"}`}>{data.reason}</p>
      </div>
      <div className="glass-card divide-y divide-slate-100">
        {[
          { l: "Blur Detection",  v: data.details.blur_score.toFixed(0),       b: blurBadge(data.details.blur_score) },
          { l: "Brightness",      v: data.details.brightness_score.toFixed(0), b: brightBadge(data.details.brightness_score) },
          { l: "Resolution",      v: data.details.resolution,                  b: ["Good", "tag-green"] as [string, string] },
          { l: "Field Coverage",  v: "Macula Centered",                        b: ["Good", "tag-green"] as [string, string] },
        ].map(({ l, v, b }) => (
          <div key={l} className="flex items-center justify-between p-3.5">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{l}</span>
            <div className="flex items-center gap-3">
              <span className="text-sm font-bold text-slate-800">{v}</span>
              <span className={`tag ${b[1]}`}>{b[0]}</span>
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
};

/* Diagnosis */
const DiagnosisPanel: React.FC<{ result: PredictionResult }> = ({ result }) => {
  const labels  = ["No DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "Proliferative DR"];
  const tagCls  = ["tag-green", "tag-amber", "tag-amber", "tag-red", "tag-red"];
  const numCol  = ["#16A34A", "#D97706", "#D97706", "#EA580C", "#DC2626"];

  return (
    <Panel iconColor="#3B82F6" title="AI Diagnosis Summary" icon={<Activity className="w-4 h-4" />}>
      <div className="glass-card p-5 mb-5 relative overflow-hidden"
        style={{ background: `linear-gradient(135deg, rgba(59,130,246,0.05) 0%, rgba(139,92,246,0.05) 100%)` }}>
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Activity className="w-32 h-32 text-blue-900" />
        </div>
        <div className="flex items-center gap-5 relative z-10">
          <div className="text-center">
            <div className="text-6xl font-black leading-none drop-shadow-sm" style={{ color: numCol[result.grade] }}>{result.grade}</div>
            <div className="text-[11px] font-bold text-slate-400 mt-2 tracking-widest uppercase">Grade</div>
          </div>
          <div>
            <span className={`tag ${tagCls[result.grade]} text-xs mb-3 inline-block px-3 py-1.5`}>{labels[result.grade]}</span>
            <p className="text-xs text-slate-500 uppercase tracking-wide">
              Confidence: <strong className="text-slate-900 text-lg ml-1">{(result.confidence * 100).toFixed(1)}%</strong>
            </p>
          </div>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-3">
        {[
          { icon: <Clock className="w-4 h-4 text-blue-500" />,   label: "Inference Time", value: `${result.processing_time.toFixed(2)}s` },
          { icon: <Cpu className="w-4 h-4 text-violet-500" />,   label: "Device",         value: "GPU CUDA" },
          { icon: <Zap className="w-4 h-4 text-amber-500" />,    label: "Model",          value: "EN-B3 v1.0" },
        ].map(({ icon, label, value }) => (
          <div key={label} className="glass-card p-3 text-center transition-colors hover:bg-white/40">
            <div className="flex justify-center mb-2">{icon}</div>
            <div className="text-sm font-bold text-slate-800 mb-0.5">{value}</div>
            <div className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">{label}</div>
          </div>
        ))}
      </div>
    </Panel>
  );
};

/* Probability */
const ProbabilityPanel: React.FC<{ probs: number[] }> = ({ probs }) => {
  const classes = [
    { name: "No DR",         fill: "linear-gradient(90deg, #10B981, #34D399)" },
    { name: "Mild NPDR",     fill: "linear-gradient(90deg, #EAB308, #FDE047)" },
    { name: "Moderate NPDR", fill: "linear-gradient(90deg, #F59E0B, #FBBF24)" },
    { name: "Severe NPDR",   fill: "linear-gradient(90deg, #F97316, #FDBA74)" },
    { name: "Proliferative", fill: "linear-gradient(90deg, #EF4444, #F87171)" },
  ];
  return (
    <Panel iconColor="#8B5CF6" title="Probability Distribution — DR Grade Likelihood" icon={<BarChart3 className="w-4 h-4" />}>
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-5">
        {classes.map((c, i) => {
          const pct = (probs[i] || 0) * 100;
          return (
            <div key={i} className="glass-card p-4 flex flex-col justify-center relative overflow-hidden group">
              <div className="flex justify-between items-baseline mb-3 relative z-10">
                <span className="text-xs font-bold text-slate-600 tracking-wide">{c.name}</span>
                <span className="text-lg font-black text-slate-900">{pct.toFixed(1)}%</span>
              </div>
              <div className="bar-track relative z-10">
                <div className="bar-fill shadow-sm" style={{ width: `${pct}%`, background: c.fill }} />
              </div>
            </div>
          );
        })}
      </div>
    </Panel>
  );
};

/* Grad-CAM */
const GradCamPanel: React.FC<{ original: string; heatmap: string | null }> = ({ original, heatmap }) => {
  const [fs, setFs]     = useState(false);
  const [zoom, setZoom] = useState(false);

  return (
    <>
      <Panel iconColor="#F43F5E" title="Grad-CAM Explainability Visualization" icon={<Eye className="w-4 h-4" />}>
        <div className="flex justify-end gap-2 mb-4">
          <button className="btn-sm btn-sm-white" onClick={() => setZoom(z => !z)}>
            <ZoomIn className="w-4 h-4" /> {zoom ? "Reset" : "Zoom"}
          </button>
          {heatmap && (
            <button className="btn-sm btn-sm-white" onClick={() => setFs(true)}>
              <Maximize className="w-4 h-4" /> Fullscreen
            </button>
          )}
          {heatmap && (
            <button className="btn-sm btn-sm-blue" onClick={() => {
              const a = document.createElement("a"); a.href = heatmap;
              a.download = "gradcam.jpg"; a.click();
            }}>
              <Download className="w-4 h-4" /> Download
            </button>
          )}
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="glass-card p-3">
            <p className="text-[11px] font-bold text-slate-400 uppercase mb-2 text-center tracking-widest">Original Scan</p>
            <div className="bg-slate-900 rounded-xl aspect-square overflow-hidden border border-slate-200">
              <img src={original} alt="original" className="w-full h-full object-contain opacity-95 hover:opacity-100 transition-opacity" />
            </div>
          </div>
          <div className="glass-card p-3 border-rose-200 shadow-[0_0_15px_rgba(244,63,114,0.05)]">
            <p className="text-[11px] font-bold text-rose-500 uppercase mb-2 text-center tracking-widest">Grad-CAM Overlay</p>
            {heatmap ? (
              <div className={`bg-slate-900 rounded-xl aspect-square overflow-hidden border border-rose-200 transition-transform duration-500 ${zoom ? "scale-110 relative z-10 shadow-2xl" : ""}`}>
                <img src={heatmap} alt="heatmap" className="w-full h-full object-contain" />
              </div>
            ) : (
              <div className="bg-rose-50 rounded-xl aspect-square border border-dashed border-rose-200 flex flex-col items-center justify-center">
                <Loader2 className="w-6 h-6 text-rose-400 animate-spin mb-2" />
                <p className="text-[10px] text-rose-400 font-bold uppercase tracking-widest">Generating</p>
              </div>
            )}
          </div>
        </div>
        <div className="mt-4 flex gap-3 items-start p-3 bg-rose-50 border border-rose-100 rounded-xl">
          <Info className="w-4 h-4 text-rose-500 flex-shrink-0 mt-0.5" />
          <p className="text-[12px] text-rose-700 leading-relaxed font-medium">
            Hot regions (red/yellow) highlight the most critical retinal areas weighted by the Convolutional Neural Network for grading.
          </p>
        </div>
      </Panel>
      {fs && heatmap && (
        <div className="fixed inset-0 z-[999] bg-slate-900/90 backdrop-blur-md flex flex-col items-center justify-center p-4"
          onClick={() => setFs(false)}>
          <p className="text-white text-sm font-bold mb-6 tracking-widest uppercase shadow-sm">Click anywhere to close</p>
          <img src={heatmap} alt="Grad-CAM fullscreen"
            className="max-h-[85vh] max-w-[95vw] object-contain rounded-2xl shadow-2xl border border-slate-700" />
        </div>
      )}
    </>
  );
};

/* Clinical Findings */
const FindingsPanel: React.FC<{ findings: string[] }> = ({ findings }) => {
  const lesions = [
    { name: "Microaneurysms",       kw: "microaneurysm" },
    { name: "Dot/Blot Hemorrhages", kw: "hemorrhage" },
    { name: "Hard Exudates",        kw: "exudate" },
    { name: "Cotton Wool Spots",    kw: "cotton wool" },
    { name: "IRMA",                 kw: "irma" },
    { name: "Neovascularization",   kw: "neovascularization" },
  ];
  const text = findings.join(" ").toLowerCase();

  return (
    <Panel iconColor="#F59E0B" title="Clinical Findings — Lesion Detection" icon={<Microscope className="w-4 h-4" />}>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-5">
        {lesions.map(({ name, kw }) => {
          const det = text.includes(kw);
          return (
            <div key={name}
              className={`flex items-center gap-3 p-3 rounded-xl border ${det ? "bg-amber-50 border-amber-200 shadow-sm" : "glass-card opacity-80"}`}>
              {det
                ? <div className="w-7 h-7 rounded-full bg-amber-100 flex items-center justify-center"><CheckCircle2 className="w-4 h-4 text-amber-600" /></div>
                : <div className="w-7 h-7 rounded-full bg-slate-100 flex items-center justify-center"><XCircle className="w-4 h-4 text-slate-400" /></div>}
              <div>
                <p className={`text-[11px] font-bold leading-tight ${det ? "text-amber-900" : "text-slate-500"}`}>{name}</p>
                <p className={`text-[9px] font-black uppercase tracking-wider ${det ? "text-amber-600" : "text-slate-400"}`}>
                  {det ? "Detected" : "Absent"}
                </p>
              </div>
            </div>
          );
        })}
      </div>
      <p className="text-[11px] font-bold text-slate-400 uppercase mb-3 tracking-widest">AI Observation Notes</p>
      <div className="space-y-2 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
        {findings.map((f, i) => (
          <div key={i} className="flex gap-2.5 text-[12px] text-slate-700 glass-card px-3.5 py-3 items-start">
            <ChevronRight className="w-4 h-4 text-blue-500 flex-shrink-0 mt-0.5" />
            <span className="leading-relaxed font-medium">{f}</span>
          </div>
        ))}
      </div>
    </Panel>
  );
};

/* Recommendation */
const RecommendationPanel: React.FC<{ grade: number; recs: string[] }> = ({ grade, recs }) => {
  const cfg = [
    { risk: "Minimal",  clr: "#059669", bg: "rgba(16, 185, 129, 0.05)", border: "rgba(16, 185, 129, 0.2)", interval: "Annual",    ref: "Primary Care",      next: "1 year"   },
    { risk: "Mild",     clr: "#D97706", bg: "rgba(245, 158, 11, 0.05)", border: "rgba(245, 158, 11, 0.2)", interval: "6 Months",  ref: "Optometrist",       next: "6 months" },
    { risk: "Moderate", clr: "#D97706", bg: "rgba(245, 158, 11, 0.1)",  border: "rgba(245, 158, 11, 0.3)", interval: "3 Months",  ref: "Ophthalmologist",   next: "3 months" },
    { risk: "High",     clr: "#EA580C", bg: "rgba(249, 115, 22, 0.1)",  border: "rgba(249, 115, 22, 0.3)", interval: "2-4 Weeks", ref: "Retinal Specialist", next: "2-4 wks" },
    { risk: "Critical", clr: "#DC2626", bg: "rgba(239, 68, 68, 0.1)",   border: "rgba(239, 68, 68, 0.3)",  interval: "Immediate", ref: "Emergency Retinal", next: "ASAP"     },
  ][grade] ?? { risk: "—", clr: "#64748B", bg: "rgba(255,255,255,0.5)", border: "rgba(255,255,255,0.8)", interval: "—", ref: "—", next: "—" };

  return (
    <Panel iconColor="#10B981" title="Clinical Recommendation — Management Plan" icon={<Stethoscope className="w-4 h-4" />}>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Risk Level",     value: cfg.risk,     icon: <AlertTriangle className="w-4 h-4" /> },
          { label: "Follow-up",      value: cfg.interval, icon: <Calendar className="w-4 h-4" /> },
          { label: "Referral",       value: cfg.ref,      icon: <ClipboardList className="w-4 h-4" /> },
          { label: "Next Screening", value: cfg.next,     icon: <TrendingUp className="w-4 h-4" /> },
        ].map(({ label, value, icon }) => (
          <div key={label} className="rounded-2xl p-4 transition-transform hover:scale-[1.02]"
            style={{ background: cfg.bg, border: `1px solid ${cfg.border}` }}>
            <div className="flex items-center gap-2 mb-2 opacity-80" style={{ color: cfg.clr }}>
              {icon}<span className="text-[10px] font-bold uppercase tracking-widest">{label}</span>
            </div>
            <p className="text-lg font-black tracking-wide" style={{ color: cfg.clr }}>{value}</p>
          </div>
        ))}
      </div>
      <p className="text-[11px] font-bold text-slate-400 uppercase mb-3 tracking-widest">Detailed Management Plan</p>
      <div className="space-y-2.5">
        {recs.map((r, i) => (
          <div key={i} className="flex gap-3 text-[13px] text-slate-700 glass-card px-4 py-3 items-start">
            <span className="font-black text-emerald-600 flex-shrink-0">{i + 1}.</span>
            <span className="leading-relaxed font-medium">{r}</span>
          </div>
        ))}
      </div>
    </Panel>
  );
};

/* Action Strip */
const ActionStrip: React.FC<{
  hasResult: boolean; sessionId: string | null; patient: PatientData;
}> = ({ hasResult, sessionId, patient }) => {
  if (!hasResult) return null;

  const downloadPdf = async () => {
    if (!sessionId) return;
    const form = new FormData();
    form.append("session_id", sessionId);
    form.append("patient_data", JSON.stringify(patient));
    try {
      const res = await fetch("/api/generate-report", { method: "POST", body: form });
      if (!res.ok) throw new Error();
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = `RetinaScan_${patient.patientId}.pdf`;
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    } catch { alert("PDF generation failed."); }
  };

  return (
    <div className="panel no-print">
      <div className="panel-body py-4">
        <div className="flex flex-wrap gap-3 items-center justify-center sm:justify-start">
          <button className="btn-sm btn-sm-blue px-6 py-2.5 text-sm" onClick={downloadPdf}>
            <FileText className="w-4 h-4" /> Generate PDF Report
          </button>
          <button className="btn-sm btn-sm-white px-5 py-2.5" onClick={downloadPdf}>
            <Download className="w-4 h-4" /> Download PDF
          </button>
          <button className="btn-sm btn-sm-white px-5 py-2.5" onClick={() => window.print()}>
            <Printer className="w-4 h-4" /> Print
          </button>
          <button className="btn-sm btn-sm-white px-5 py-2.5" disabled>
            <Code2 className="w-4 h-4" /> Export JSON
          </button>
        </div>
      </div>
    </div>
  );
};

/* ═══════════════════════════════════════════════════════════════
   APP ROOT
═══════════════════════════════════════════════════════════════ */
export default function App() {
  const [patient, setPatient] = useState<PatientData>({
    patientId: "", patientName: "", age: "", gender: "", eye: "",
    diabetesDuration: "", hba1c: "", referringDoctor: "", hospital: "",
    examinationDate: new Date().toISOString().split("T")[0],
  });
  const [imgFile, setImgFile]     = useState<File | null>(null);
  const [imgPreview, setPreview]  = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [quality, setQuality]     = useState<QualityResult | null>(null);
  const [result, setResult]       = useState<PredictionResult | null>(null);
  const [gradcam, setGradcam]     = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [loadingText, setLoading] = useState("");
  const [apiError, setApiError]   = useState<string | null>(null);

  useEffect(() => () => {
    if (imgPreview?.startsWith("blob:")) URL.revokeObjectURL(imgPreview);
  }, [imgPreview]);

  const handleImage = useCallback((f: File | null, p: string | null, b: string | null) => {
    if (imgPreview?.startsWith("blob:")) URL.revokeObjectURL(imgPreview);
    setImgFile(f); setPreview(p);
    setSessionId(null); setQuality(null); setResult(null); setGradcam(null); setApiError(null);
  }, [imgPreview]);

  const isReady = !!imgFile &&
    patient.patientId.trim() !== "" && patient.patientName.trim() !== "" &&
    patient.age.trim() !== "" && patient.gender !== "" &&
    patient.eye !== "" && patient.examinationDate.trim() !== "";

  const analyze = async () => {
    if (!imgFile) return;
    setAnalyzing(true); setApiError(null);
    try {
      setLoading("Establishing secure connection…");
      const fd = new FormData(); fd.append("image", imgFile);
      const upRes = await fetch("/api/upload", { method: "POST", body: fd });
      if (!upRes.ok) throw new Error("Image upload failed.");
      const { session_id } = await upRes.json();
      setSessionId(session_id);

      setLoading("Assessing image quality metrics…");
      const sf = new FormData(); sf.append("session_id", session_id);
      const qRes = await fetch("/api/image-quality", { method: "POST", body: sf });
      if (!qRes.ok) throw new Error("Quality assessment failed.");
      const qData: QualityResult = await qRes.json();
      setQuality(qData);
      if (!qData.is_pass) throw new Error(qData.reason);

      setLoading("Running deep neural network inference…");
      const pRes = await fetch("/api/predict", { method: "POST", body: sf });
      if (!pRes.ok) throw new Error("Prediction failed.");
      const pData: PredictionResult = await pRes.json();
      setResult(pData);

      setLoading("Generating Grad-CAM visualization…");
      fetch("/api/gradcam", { method: "POST", body: sf })
        .then(r => r.json())
        .then(d => { if (d.gradcam_base64) setGradcam(d.gradcam_base64); })
        .catch(() => {});
    } catch (e: any) {
      setApiError(e.message || "Unexpected error during AI analysis.");
    } finally { setAnalyzing(false); setLoading(""); }
  };

  return (
    <div className="page">
      {/* ── Header Title replacing Topbar ── */}
      <div className="mb-8 text-center no-print pt-4">
        <h1 className="text-3xl sm:text-4xl font-black text-slate-800 tracking-tight mb-2">Diabetic Retinopathy AI</h1>
        <p className="text-slate-500 font-semibold tracking-wide">Model: EfficientNet-B3 · v1.0 Enterprise</p>
      </div>

      {/* ── Row 1: Patient Info ── */}
      <div className="mb-6">
        <PatientPanel data={patient} onChange={setPatient} />
      </div>

      {/* ── Row 2: Image Upload ── */}
      <div className="mb-6">
        <ImagePanel file={imgFile} preview={imgPreview} onChange={handleImage} />
      </div>

      {/* ── Analyze Bar ── */}
      <div className="mb-6 no-print">
        <AnalyzeSection
          isReady={isReady} isAnalyzing={analyzing}
          loadingText={loadingText} onAnalyze={analyze}
        />
      </div>

      {/* ── Error ── */}
      {apiError && (
        <div className="mb-6 flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-800 text-sm font-medium shadow-sm">
          <AlertTriangle className="w-5 h-5 flex-shrink-0 text-red-600" />{apiError}
        </div>
      )}

      {/* ── Results (only after analysis) ── */}
      {result && (
        <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
          {/* Quality + Diagnosis */}
          <div className="result-row cols-2">
            {quality && <QualityPanel data={quality} />}
            <DiagnosisPanel result={result} />
          </div>

          {/* Probability full-width */}
          <div className="result-row cols-1">
            <ProbabilityPanel probs={result.probabilities} />
          </div>

          {/* Grad-CAM + Findings */}
          <div className="result-row cols-2">
            <GradCamPanel original={imgPreview!} heatmap={gradcam} />
            <FindingsPanel findings={result.findings} />
          </div>

          {/* Recommendation full-width */}
          <div className="result-row cols-1">
            <RecommendationPanel grade={result.grade} recs={result.recommendations} />
          </div>

          {/* Action buttons */}
          <div className="mb-6">
            <ActionStrip hasResult={!!result} sessionId={sessionId} patient={patient} />
          </div>

          {/* Disclaimer */}
          <div className="flex gap-3 items-start p-4 bg-slate-50 border border-slate-200 rounded-2xl shadow-sm">
            <Info className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
            <p className="text-xs text-slate-500 leading-relaxed font-medium">
              <strong className="text-slate-700">Medical Disclaimer:</strong> This AI system is for screening and decision-support only.
              All findings must be confirmed by a qualified ophthalmologist. Model: EfficientNet-B3 · EN-B3-DR-v1.0.
            </p>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="mt-12 pt-6 border-t border-slate-200 no-print">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-xs text-slate-400 font-medium tracking-wide">&copy; {new Date().getFullYear()} Ophthalmology AI Platform</p>
          <div className="flex gap-5">
            {["Privacy", "Disclaimer", "Support"].map(l => (
              <a key={l} href="#" className="text-xs text-slate-500 hover:text-blue-600 font-semibold transition-colors">{l}</a>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}
