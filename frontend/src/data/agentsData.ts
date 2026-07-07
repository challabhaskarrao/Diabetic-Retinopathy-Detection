import { IAgent } from '../types/agent';

export const agentsData: IAgent[] = [
  {
    id: 'diabetic-retinopathy',
    name: 'Diabetic Retinopathy',
    description: 'Automated grading of diabetic retinopathy severity from fundus images using multi-scale convolutional neural networks validated against clinical gold standards.',
    category: 'Retinal Imaging',
    accuracy: 98.5,
    time: '< 2s',
    formats: ['JPEG', 'PNG', 'DICOM'],
    icon: 'Eye'
  },
  {
    id: 'handheld-portable-oct',
    name: 'Handheld Portable OCT',
    description: 'AI-assisted interpretation of optical coherence tomography scans acquired with handheld devices — enabling bedside, outreach, and pediatric retinal assessments.',
    category: 'OCT Analysis',
    accuracy: 97.2,
    time: '< 3s',
    formats: ['DICOM', 'TIFF', 'PNG'],
    icon: 'ScanFace'
  },
  {
    id: 'pediatric-retinal-imaging',
    name: 'Pediatric Retinal Imaging',
    description: 'Specialized deep-learning model for detecting retinopathy of prematurity (ROP), congenital abnormalities, and other pediatric retinal pathologies.',
    category: 'Pediatric Ophthalmology',
    accuracy: 96.8,
    time: '< 3s',
    formats: ['JPEG', 'PNG', 'DICOM'],
    icon: 'Eye'
  },
  {
    id: '3d-ocular-ultrasound',
    name: '3D Ocular Ultrasound',
    description: 'Volumetric analysis of 3D B-scan ultrasound data for detecting vitreoretinal pathologies, choroidal lesions, and posterior segment disorders.',
    category: 'Ocular Imaging',
    accuracy: 95.4,
    time: '< 6s',
    formats: ['DICOM', 'NIfTI'],
    icon: 'Brain'
  },
  {
    id: 'portable-fundus-fluorescein-angiography',
    name: 'Portable Fundus Fluorescein Angiography',
    description: 'Automated identification of leakage patterns, neovascularization, and capillary non-perfusion zones from FFA images captured with portable fundus cameras.',
    category: 'Retinal Imaging',
    accuracy: 97.1,
    time: '< 4s',
    formats: ['JPEG', 'PNG', 'DICOM'],
    icon: 'Eye'
  },
  {
    id: 'portable-auto-refractometer',
    name: 'Portable Auto-refractometer',
    description: 'Intelligent refractive error analysis from portable auto-refractor data, providing accurate sphere, cylinder, and axis measurements for clinical decision support.',
    category: 'Refractive Analysis',
    accuracy: 99.1,
    time: '< 1s',
    formats: ['JSON', 'CSV', 'XML'],
    icon: 'Stethoscope'
  },
  {
    id: 'portable-non-invasive-tonometer',
    name: 'Portable Non-invasive Tonometer',
    description: 'AI-powered intraocular pressure trend analysis from non-contact tonometry data for early glaucoma risk stratification and monitoring.',
    category: 'Glaucoma Screening',
    accuracy: 96.3,
    time: '< 2s',
    formats: ['JSON', 'CSV'],
    icon: 'Activity'
  },
  {
    id: 'optic-nerve-disease-detection',
    name: 'Optic Nerve Disease Detection',
    description: 'Precision segmentation and classification of optic disc and cup morphology to detect glaucoma, papilledema, optic neuritis, and related neuropathies.',
    category: 'Glaucoma Screening',
    accuracy: 97.8,
    time: '< 3s',
    formats: ['JPEG', 'PNG', 'DICOM'],
    icon: 'ScanFace'
  },
  {
    id: 'amblyopia',
    name: 'Amblyopia Detection',
    description: 'Early-stage amblyopia screening using red reflex imaging and ocular alignment analysis, optimized for pediatric community outreach programs.',
    category: 'Pediatric Ophthalmology',
    accuracy: 95.6,
    time: '< 2s',
    formats: ['JPEG', 'PNG'],
    icon: 'Eye'
  },
  {
    id: 'universal-eye-screening',
    name: 'Universal Eye Screening Device',
    description: 'Comprehensive multimodal AI screening platform that simultaneously assesses refractive error, disc abnormalities, retinal pathology, and visual acuity for large-scale population screening.',
    category: 'Multi-condition Screening',
    accuracy: 98.0,
    time: '< 5s',
    formats: ['JPEG', 'PNG', 'DICOM', 'JSON'],
    icon: 'Brain'
  }
];

export const categories = [
  'All',
  'Retinal Imaging',
  'OCT Analysis',
  'Pediatric Ophthalmology',
  'Ocular Imaging',
  'Refractive Analysis',
  'Glaucoma Screening',
  'Multi-condition Screening'
];
