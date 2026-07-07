import { motion } from 'motion/react';
import { fadeUpVariant, staggerContainer } from '../animations/variants';
import { Target, Zap, Shield, Lock, FlaskConical, Layers } from 'lucide-react';

export const FeaturesSection = () => {
  const features = [
    {
      icon: Target,
      title: "High Accuracy",
      description: "Models trained on millions of annotated medical images achieving human-level or superhuman performance."
    },
    {
      icon: Zap,
      title: "Fast Predictions",
      description: "Optimized inference pipelines deliver diagnostic results in under 5 seconds."
    },
    {
      icon: Shield,
      title: "Privacy First",
      description: "HIPAA compliant architecture. Patient data is never stored without explicit consent."
    },
    {
      icon: Lock,
      title: "Secure infrastructure",
      description: "End-to-end encryption for all data transmission and storage processes."
    },
    {
      icon: FlaskConical,
      title: "Research Based",
      description: "Algorithms grounded in peer-reviewed clinical studies and cutting-edge ML research."
    },
    {
      icon: Layers,
      title: "Multi-Disease Support",
      description: "A single unified platform for oncology, ophthalmology, pulmonology and more."
    }
  ];

  return (
    <section className="py-24 relative bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeUpVariant}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-slate-900">
            Why Choose <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-sky-500">NovaMed</span>
          </h2>
        </motion.div>

        <motion.div 
          variants={staggerContainer}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feature, i) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={i}
                variants={fadeUpVariant}
                whileHover={{ y: -5 }}
                className="bg-white p-8 rounded-2xl border border-slate-200 hover:border-blue-300 hover:shadow-lg transition-all group"
              >
                <div className="w-12 h-12 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center mb-6 group-hover:bg-blue-100 transition-colors">
                  <Icon className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
};
