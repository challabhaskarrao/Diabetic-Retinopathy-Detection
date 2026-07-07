import { motion } from 'motion/react';
import { UploadCloud, Cpu, Microscope, Zap, FileText } from 'lucide-react';
import { fadeUpVariant, staggerContainer } from '../animations/variants';

export const WorkflowSection = () => {
  const steps = [
    {
      icon: UploadCloud,
      title: "Upload Image",
      description: "Securely upload clinical imagery (DICOM, PNG, JPEG)."
    },
    {
      icon: Cpu,
      title: "AI Processing",
      description: "Data is pre-processed and normalized for the specific neural network."
    },
    {
      icon: Microscope,
      title: "Deep Learning Analysis",
      description: "State-of-the-art vision models extract intricate pathological features."
    },
    {
      icon: Zap,
      title: "Prediction",
      description: "Probability distributions are calculated for potential diagnoses."
    },
    {
      icon: FileText,
      title: "Generate Report",
      description: "A comprehensive, interpretable clinical report is generated."
    }
  ];

  return (
    <section id="workflow" className="py-24 relative overflow-hidden bg-white">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[300px] bg-blue-100/50 blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeUpVariant}
          className="text-center mb-20"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-slate-900">
            Streamlined <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-sky-500">Diagnostic Pipeline</span>
          </h2>
          <p className="text-slate-600 max-w-2xl mx-auto text-lg">
            From image upload to clinical report in seconds. Our optimized architecture ensures minimal latency and maximum throughput.
          </p>
        </motion.div>

        <div className="relative">
          {/* Connecting Line (Desktop) */}
          <div className="hidden lg:block absolute top-12 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-blue-200 to-transparent" />

          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="grid grid-cols-1 lg:grid-cols-5 gap-8 lg:gap-4 relative"
          >
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <motion.div 
                  key={index} 
                  variants={fadeUpVariant}
                  className="flex flex-col items-center text-center relative group"
                >
                  <div className="w-24 h-24 rounded-full bg-white border border-slate-200 shadow-sm flex items-center justify-center mb-6 relative z-10 group-hover:border-blue-300 group-hover:bg-blue-50 transition-all duration-300">
                    <Icon className="w-10 h-10 text-blue-600 group-hover:scale-110 transition-transform duration-300" />
                    
                    {/* Step Number Badge */}
                    <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold border-4 border-white shadow-sm">
                      {index + 1}
                    </div>
                  </div>
                  
                  <h3 className="text-lg font-bold text-slate-900 mb-3">{step.title}</h3>
                  <p className="text-sm text-slate-600">{step.description}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </div>
    </section>
  );
};
