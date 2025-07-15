import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { 
  Calculator, 
  Activity, 
  User, 
  Weight,
  Ruler,
  Calendar,
  TrendingUp,
  AlertCircle,
  Info,
  Sparkles
} from 'lucide-react';

import { 
  AssessmentFormData, 
  RiskAssessmentRequest, 
  FormErrors,
  LoadingState 
} from '../types';
import { 
  calculateBMI, 
  getBMICategory, 
  parseStepData, 
  validateAge, 
  validateBMI, 
  validateStepData,
  generateSampleStepData,
  formatNumber 
} from '../utils';

interface RiskAssessmentFormProps {
  onSubmit: (data: RiskAssessmentRequest) => Promise<void>;
  loading: LoadingState;
}

const RiskAssessmentForm: React.FC<RiskAssessmentFormProps> = ({
  onSubmit,
  loading
}) => {
  const [formData, setFormData] = useState<AssessmentFormData>({
    age: '',
    weight: '',
    height: '',
    stepData: '',
    gender: ''
  });
  
  const [bmi, setBmi] = useState<number>(0);
  const [stepCount, setStepCount] = useState<number>(0);
  const [errors, setErrors] = useState<FormErrors>({});
  const [showStepExample, setShowStepExample] = useState(false);

  // Calculate BMI when weight or height changes
  useEffect(() => {
    const weight = parseFloat(formData.weight);
    const height = parseFloat(formData.height);
    if (weight > 0 && height > 0) {
      const calculatedBMI = calculateBMI(weight, height);
      setBmi(calculatedBMI);
    } else {
      setBmi(0);
    }
  }, [formData.weight, formData.height]);

  // Count valid step entries
  useEffect(() => {
    if (formData.stepData.trim()) {
      const steps = parseStepData(formData.stepData);
      setStepCount(steps.length);
    } else {
      setStepCount(0);
    }
  }, [formData.stepData]);

  const handleInputChange = (field: keyof AssessmentFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Age validation
    const age = parseInt(formData.age);
    if (!formData.age || isNaN(age)) {
      newErrors.age = 'Age is required';
    } else if (!validateAge(age)) {
      newErrors.age = 'Age must be between 18 and 100 years';
    }

    // Weight validation
    const weight = parseFloat(formData.weight);
    if (!formData.weight || isNaN(weight)) {
      newErrors.weight = 'Weight is required';
    } else if (weight < 30 || weight > 300) {
      newErrors.weight = 'Weight must be between 30 and 300 kg';
    }

    // Height validation
    const height = parseFloat(formData.height);
    if (!formData.height || isNaN(height)) {
      newErrors.height = 'Height is required';
    } else if (height < 100 || height > 250) {
      newErrors.height = 'Height must be between 100 and 250 cm';
    }

    // BMI validation
    if (bmi > 0 && !validateBMI(bmi)) {
      newErrors.bmi = 'BMI appears to be outside normal range (10-60)';
    }

    // Step data validation
    if (!formData.stepData.trim()) {
      newErrors.stepData = 'Step data is required';
    } else {
      const steps = parseStepData(formData.stepData);
      if (steps.length < 14) {
        newErrors.stepData = 'Please provide at least 14 days of step data';
      } else if (steps.length > 28) {
        newErrors.stepData = 'Please provide no more than 28 days of step data';
      } else if (!validateStepData([...steps, ...Array(28 - steps.length).fill(0)])) {
        newErrors.stepData = 'Some step counts appear invalid (0-50,000 steps/day)';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const steps = parseStepData(formData.stepData);
    // Pad with zeros if less than 28 days, or take first 28 if more
    let stepData = steps.length >= 28 
      ? steps.slice(0, 28)
      : [...steps, ...Array(28 - steps.length).fill(0)];
    
    // Ensure all values are valid (0-100000)
    stepData = stepData.map(steps => Math.max(0, Math.min(100000, steps)));

    const requestData: RiskAssessmentRequest = {
      age: Math.max(1, Math.min(120, parseInt(formData.age))),
      bmi: Math.max(10.0, Math.min(60.0, bmi)),
      past_28_day_steps: stepData
    };

    console.log('📊 Sending request data:', JSON.stringify(requestData, null, 2));
    console.log('Step data length:', stepData.length);
    console.log('Step data sample:', stepData.slice(0, 5));

    await onSubmit(requestData);
  };

  const fillSampleData = () => {
    const sampleSteps = generateSampleStepData(7000, 2000);
    const sampleStepString = sampleSteps.map((steps, index) => 
      `Day ${index + 1}: ${steps} steps`
    ).join('\n');

    setFormData({
      age: '45',
      weight: '75',
      height: '175',
      stepData: sampleStepString,
      gender: 'other'
    });
  };

  const bmiCategory = bmi > 0 ? getBMICategory(bmi) : null;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="card">
        <div className="card-header">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Calculator className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-secondary-900">
                Diabetes Risk Assessment
              </h2>
              <p className="text-sm text-secondary-600">
                AI-powered health analysis with personalized recommendations
              </p>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="card-body space-y-6">
          {/* Personal Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-secondary-900 flex items-center gap-2">
              <User className="w-5 h-5 text-secondary-600" />
              Personal Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Age */}
              <div>
                <label className="label">
                  <Calendar className="w-4 h-4 inline mr-1" />
                  Age (years)
                </label>
                <input
                  type="number"
                  className={`input ${errors.age ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
                  placeholder="e.g., 45"
                  value={formData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  min="18"
                  max="100"
                />
                {errors.age && (
                  <p className="text-sm text-danger-600 mt-1 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    {errors.age}
                  </p>
                )}
              </div>

              {/* Weight */}
              <div>
                <label className="label">
                  <Weight className="w-4 h-4 inline mr-1" />
                  Weight (kg)
                </label>
                <input
                  type="number"
                  step="0.1"
                  className={`input ${errors.weight ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
                  placeholder="e.g., 75.5"
                  value={formData.weight}
                  onChange={(e) => handleInputChange('weight', e.target.value)}
                  min="30"
                  max="300"
                />
                {errors.weight && (
                  <p className="text-sm text-danger-600 mt-1 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    {errors.weight}
                  </p>
                )}
              </div>

              {/* Height */}
              <div>
                <label className="label">
                  <Ruler className="w-4 h-4 inline mr-1" />
                  Height (cm)
                </label>
                <input
                  type="number"
                  step="0.1"
                  className={`input ${errors.height ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
                  placeholder="e.g., 175"
                  value={formData.height}
                  onChange={(e) => handleInputChange('height', e.target.value)}
                  min="100"
                  max="250"
                />
                {errors.height && (
                  <p className="text-sm text-danger-600 mt-1 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    {errors.height}
                  </p>
                )}
              </div>
            </div>

            {/* BMI Display */}
            {bmi > 0 && (
              <div className={`p-4 rounded-lg border ${
                bmiCategory?.color === 'success' ? 'bg-success-50 border-success-200' :
                bmiCategory?.color === 'warning' ? 'bg-warning-50 border-warning-200' :
                'bg-danger-50 border-danger-200'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">
                      BMI: {bmi} kg/m²
                    </p>
                    <p className="text-sm opacity-75">
                      Category: {bmiCategory?.category} ({bmiCategory?.range})
                    </p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                    bmiCategory?.color === 'success' ? 'bg-success-100 text-success-800' :
                    bmiCategory?.color === 'warning' ? 'bg-warning-100 text-warning-800' :
                    'bg-danger-100 text-danger-800'
                  }`}>
                    {bmiCategory?.category}
                  </div>
                </div>
                {errors.bmi && (
                  <p className="text-sm text-danger-600 mt-2 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    {errors.bmi}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Activity Data */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-secondary-900 flex items-center gap-2">
                <Activity className="w-5 h-5 text-secondary-600" />
                Activity Data (Past 28 Days)
              </h3>
              <button
                type="button"
                onClick={() => setShowStepExample(!showStepExample)}
                className="btn btn-secondary text-xs"
              >
                <Info className="w-3 h-3 mr-1" />
                {showStepExample ? 'Hide' : 'Show'} Example
              </button>
            </div>

            {showStepExample && (
              <div className="bg-secondary-50 border border-secondary-200 rounded-lg p-4">
                <p className="text-sm text-secondary-700 mb-2">
                  <strong>Step Data Format:</strong> Enter your daily step counts (one per line)
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div>
                    <p className="font-semibold mb-1">Accepted formats:</p>
                    <div className="text-secondary-600">
                      <p>Day 1: 7500 steps</p>
                      <p>7500</p>
                      <p>Steps: 7500</p>
                      <p>2024-01-01: 7500</p>
                    </div>
                  </div>
                  <div>
                    <button
                      type="button"
                      onClick={fillSampleData}
                      className="btn btn-primary text-xs"
                    >
                      <Sparkles className="w-3 h-3 mr-1" />
                      Fill Sample Data
                    </button>
                  </div>
                </div>
              </div>
            )}

            <div>
              <label className="label">
                <TrendingUp className="w-4 h-4 inline mr-1" />
                Daily Step Counts ({stepCount}/28 days)
              </label>
              <textarea
                className={`input min-h-[120px] ${errors.stepData ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
                placeholder="Enter your daily step counts, one per line:
Day 1: 7500 steps
Day 2: 8200 steps
Day 3: 6800 steps
..."
                value={formData.stepData}
                onChange={(e) => handleInputChange('stepData', e.target.value)}
                rows={6}
              />
              {errors.stepData && (
                <p className="text-sm text-danger-600 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.stepData}
                </p>
              )}
              
              {stepCount > 0 && (
                <div className="mt-2 flex items-center gap-4 text-sm text-secondary-600">
                  <span>✅ {stepCount} days entered</span>
                  {stepCount >= 14 && (
                    <span className="text-success-600">
                      ✓ Sufficient data for analysis
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-between pt-4 border-t border-secondary-200">
            <div className="text-sm text-secondary-600">
              <Info className="w-4 h-4 inline mr-1" />
              Results include AI-powered recommendations from Claude
            </div>
            
            <button
              type="submit"
              disabled={loading.isLoading}
              className="btn btn-primary px-8 py-3 text-base font-medium"
            >
              {loading.isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {loading.message || 'Analyzing...'}
                </>
              ) : (
                <>
                  <Calculator className="w-4 h-4 mr-2" />
                  Calculate Risk & Get Recommendations
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RiskAssessmentForm; 