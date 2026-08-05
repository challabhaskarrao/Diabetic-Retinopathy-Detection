import React from "react";
import { User } from "lucide-react";

export interface PatientData {
  patientId: string;
  patientName: string;
  age: string;
  gender: string;
  eye: string;
  diabetesDuration: string;
  hba1c: string;
  referringDoctor: string;
  hospital: string;
  examinationDate: string;
}

interface PatientFormProps {
  data: PatientData;
  onChange: (data: PatientData) => void;
}

const PatientForm: React.FC<PatientFormProps> = ({ data, onChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    onChange({ ...data, [name]: value });
  };

  return (
    <div className="premium-card mb-6">
      <div className="premium-card-header">
        <div className="flex items-center gap-2">
          <User className="w-5 h-5 text-blue-600" />
          <span>Patient Information</span>
        </div>
      </div>
      
      <div className="premium-card-body">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-4">
          
          <div>
            <label className="premium-label" htmlFor="patientId">Patient ID *</label>
            <input
              type="text"
              id="patientId"
              name="patientId"
              value={data.patientId}
              onChange={handleChange}
              className="premium-input"
              placeholder="e.g. MRN-10293"
              required
            />
          </div>

          <div>
            <label className="premium-label" htmlFor="patientName">Patient Name *</label>
            <input
              type="text"
              id="patientName"
              name="patientName"
              value={data.patientName}
              onChange={handleChange}
              className="premium-input"
              placeholder="Full Name"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="premium-label" htmlFor="age">Age *</label>
              <input
                type="number"
                id="age"
                name="age"
                value={data.age}
                onChange={handleChange}
                className="premium-input"
                placeholder="Yrs"
                required
              />
            </div>
            <div>
              <label className="premium-label" htmlFor="gender">Gender *</label>
              <select
                id="gender"
                name="gender"
                value={data.gender}
                onChange={handleChange}
                className="premium-input"
                required
              >
                <option value="" disabled>Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div>
            <label className="premium-label" htmlFor="eye">Eye Examined *</label>
            <select
              id="eye"
              name="eye"
              value={data.eye}
              onChange={handleChange}
              className="premium-input"
              required
            >
              <option value="" disabled>Select Eye</option>
              <option value="OD">Right Eye (OD)</option>
              <option value="OS">Left Eye (OS)</option>
              <option value="OU">Both Eyes (OU)</option>
            </select>
          </div>

          <div>
            <label className="premium-label" htmlFor="diabetesDuration">Diabetes Duration (Yrs)</label>
            <input
              type="number"
              id="diabetesDuration"
              name="diabetesDuration"
              value={data.diabetesDuration}
              onChange={handleChange}
              className="premium-input"
              placeholder="e.g. 5"
            />
          </div>

          <div>
            <label className="premium-label" htmlFor="hba1c">HbA1c (%)</label>
            <input
              type="number"
              step="0.1"
              id="hba1c"
              name="hba1c"
              value={data.hba1c}
              onChange={handleChange}
              className="premium-input"
              placeholder="e.g. 7.5"
            />
          </div>

          <div>
            <label className="premium-label" htmlFor="referringDoctor">Referring Doctor</label>
            <input
              type="text"
              id="referringDoctor"
              name="referringDoctor"
              value={data.referringDoctor}
              onChange={handleChange}
              className="premium-input"
              placeholder="Dr. Name"
            />
          </div>

          <div>
            <label className="premium-label" htmlFor="hospital">Hospital / Clinic</label>
            <input
              type="text"
              id="hospital"
              name="hospital"
              value={data.hospital}
              onChange={handleChange}
              className="premium-input"
              placeholder="Facility Name"
            />
          </div>

          <div>
            <label className="premium-label" htmlFor="examinationDate">Visit Date *</label>
            <input
              type="date"
              id="examinationDate"
              name="examinationDate"
              value={data.examinationDate}
              onChange={handleChange}
              className="premium-input"
              required
            />
          </div>

        </div>
      </div>
    </div>
  );
};

export default PatientForm;
