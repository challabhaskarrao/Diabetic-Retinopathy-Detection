import { motion } from 'motion/react';
import { IAgent } from '../types/agent';
import { ArrowRight, Eye, ScanFace, Stethoscope, Brain, Activity, Clock, ShieldCheck, LucideIcon } from 'lucide-react';

const iconMap: Record<string, LucideIcon> = {
  Eye: Eye,
  ScanFace: ScanFace,
  Brain: Brain,
  Stethoscope: Stethoscope,
  Activity: Activity,
};

interface AgentCardProps {
  agent: IAgent;
}

export const AgentCard = ({ agent }: AgentCardProps) => {
  const IconComponent = iconMap[agent.icon] || Eye;

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="bg-white rounded-2xl p-6 group relative overflow-hidden flex flex-col h-full border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-200 transition-all duration-300"
    >
      {/* Subtle hover tint */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

      {/* Header row */}
      <div className="flex justify-between items-start mb-6 relative z-10">
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 group-hover:border-blue-300 group-hover:bg-blue-50 transition-colors">
          <IconComponent className="w-8 h-8 text-blue-600" />
        </div>
        <div className="flex flex-col items-end gap-2">
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
            <ShieldCheck className="w-3 h-3" />
            {agent.accuracy}% Acc
          </span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium border border-slate-200">
            <Clock className="w-3 h-3" />
            {agent.time}
          </span>
        </div>
      </div>

      {/* Body */}
      <div className="relative z-10 flex-grow">
        <div className="text-xs font-semibold text-blue-600 mb-2 tracking-wider uppercase">
          {agent.category}
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-blue-700 transition-colors">
          {agent.name}
        </h3>
        <p className="text-slate-600 text-sm leading-relaxed mb-6">
          {agent.description}
        </p>
      </div>

      {/* Footer */}
      <div className="relative z-10 mt-auto pt-4 border-t border-slate-100">
        <div className="flex items-center justify-between mb-4">
          <div className="text-xs text-slate-500 font-medium">Formats:</div>
          <div className="flex flex-wrap gap-1 justify-end">
            {agent.formats.map(fmt => (
              <span
                key={fmt}
                className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 border border-slate-200 text-slate-600 font-medium"
              >
                {fmt}
              </span>
            ))}
          </div>
        </div>

        <button className="w-full py-3 rounded-lg bg-slate-50 border border-slate-200 hover:bg-blue-600 hover:border-blue-600 hover:text-white text-slate-700 text-sm font-medium transition-all group-hover:shadow-[0_4px_14px_0_rgb(37,99,235,0.39)] flex justify-center items-center gap-2">
          Launch Agent
          <ArrowRight className="w-4 h-4 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all" />
        </button>
      </div>
    </motion.div>
  );
};
