// User and Assessment Types
export interface User {
  id?: string;
  age: number;
  bmi: number;
  gender?: 'male' | 'female' | 'other';
  weight?: number;
  height?: number;
}

export interface StepData {
  date: string;
  steps: number;
}

export interface RiskAssessmentRequest {
  age: number;
  bmi: number;
  past_28_day_steps: number[];
}

export interface RiskAssessmentResult {
  patient_info: {
    age: number;
    bmi: number;
    age_group: string;
  };
  risk_percentages: {
    '1_month_risk': number;
    '3_month_risk': number;
    '6_month_risk': number;
  };
  analysis: {
    baseline_risk: number;
    activity_level: 'low' | 'moderate' | 'high';
    median_daily_steps: number;
    diabetes_risk_level: 'low-risk' | 'medium-risk' | 'high-risk';
    risk_calculation_method: string;
    reason: string;
  };
  step_analysis: {
    activity_level: 'low' | 'moderate' | 'high';
    median_steps: number;
    mean_steps: number;
    total_days: number;
    valid_days: number;
    outliers_removed: number;
    min_steps: number;
    max_steps: number;
  };
}

// Claude AI Recommendation Types
export interface RecommendationRequest {
  user_profile: {
    age: number;
    bmi: number;
    activity_level: string;
    avg_daily_steps: number;
  };
  risk_data: RiskAssessmentResult;
  recommendation_type?: 'comprehensive' | 'activity_focused' | 'risk_explanation';
}

export interface RecommendationResponse {
  recommendations: string;
  model_used: string;
  timestamp: string;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
  };
}

export interface ComprehensiveRecommendations {
  user_profile: {
    age: number;
    bmi: number;
    activity_level: string;
    median_steps: number;
    diabetes_risk_level: string;
    risk_1_month: number;
    risk_3_month: number;
    risk_6_month: number;
  };
  recommendations: {
    comprehensive: {
      content: string;
      type: string;
    };
    activity_focused: {
      content: string;
      type: string;
    };
    risk_explanation: {
      content: string;
      type: string;
    };
  };
  metadata: {
    generated_at: string;
    model_used: string;
    api_usage: {
      total_input_tokens: number;
      total_output_tokens: number;
    };
  };
  risk_assessment: RiskAssessmentResult;
}

// UI Component Types
export interface FormErrors {
  [key: string]: string | undefined;
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

// Chart and Visualization Types
export interface ChartDataPoint {
  name: string;
  value: number;
  color?: string;
}

export interface HealthMetric {
  label: string;
  value: number | string;
  unit?: string;
  type: 'low' | 'moderate' | 'high' | 'neutral';
  description?: string;
}

// Activity and Health Types
export interface ActivityLevel {
  level: 'low' | 'moderate' | 'high';
  description: string;
  recommendations: string[];
}

export interface BMICategory {
  category: 'underweight' | 'normal' | 'overweight' | 'obese';
  range: string;
  color: 'success' | 'warning' | 'danger';
}

// Navigation and Route Types
export interface NavItem {
  label: string;
  path: string;
  icon?: string;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  status: 'success' | 'error';
  timestamp?: string;
}

// Form Types
export interface AssessmentFormData {
  age: string;
  weight: string;
  height: string;
  stepData: string;
  gender?: string;
}

export interface StepDataEntry {
  day: number;
  steps: number;
  isValid: boolean;
} 