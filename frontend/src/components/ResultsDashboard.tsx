import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Calendar, 
  Target,
  BarChart3,
  AlertTriangle,
  CheckCircle,
  Info,
  Clock,
  User
} from 'lucide-react';

import { RiskAssessmentResult, HealthMetric } from '../types';
import { 
  formatPercentage, 
  getRiskLevelColor, 
  createHealthMetrics, 
  formatDate,
  formatTime,
  formatNumber,
  getActivityLevel
} from '../utils';

interface ResultsDashboardProps {
  results: RiskAssessmentResult;
  onNewAssessment?: () => void;
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({
  results,
  onNewAssessment
}) => {
  const { risk_percentages, analysis, patient_data, timestamp } = results;
  
  const healthMetrics = createHealthMetrics(
    patient_data.age,
    patient_data.bmi,
    analysis.avg_daily_steps,
    risk_percentages['3_month_risk']
  );

  const activityLevel = getActivityLevel(analysis.avg_daily_steps);
  const riskColor = getRiskLevelColor(analysis.risk_level);

  const getRiskTrend = () => {
    const oneMonth = risk_percentages['1_month_risk'];
    const threeMonth = risk_percentages['3_month_risk'];
    const sixMonth = risk_percentages['6_month_risk'];
    
    if (sixMonth > threeMonth && threeMonth > oneMonth) {
      return { trend: 'increasing', icon: TrendingUp, color: 'danger' };
    } else if (sixMonth < threeMonth && threeMonth < oneMonth) {
      return { trend: 'decreasing', icon: TrendingDown, color: 'success' };
    } else {
      return { trend: 'stable', icon: TrendingUp, color: 'warning' };
    }
  };

  const riskTrend = getRiskTrend();
  const TrendIcon = riskTrend.icon;

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${
                riskColor === 'success' ? 'bg-success-100' :
                riskColor === 'warning' ? 'bg-warning-100' :
                'bg-danger-100'
              }`}>
                <BarChart3 className={`w-6 h-6 ${
                  riskColor === 'success' ? 'text-success-600' :
                  riskColor === 'warning' ? 'text-warning-600' :
                  'text-danger-600'
                }`} />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-secondary-900">
                  Diabetes Risk Assessment Results
                </h2>
                <p className="text-sm text-secondary-600 flex items-center gap-2">
                  <Clock className="w-3 h-3" />
                  Generated on {formatDate(timestamp)} at {formatTime(timestamp)}
                </p>
              </div>
            </div>
            
            {onNewAssessment && (
              <button
                onClick={onNewAssessment}
                className="btn btn-secondary"
              >
                New Assessment
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Risk Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* 1-Month Risk */}
        <div className="card">
          <div className="card-body text-center">
            <div className="mb-4">
              <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold ${
                getRiskLevelColor(analysis.risk_level) === 'success' ? 'bg-success-100 text-success-800' :
                getRiskLevelColor(analysis.risk_level) === 'warning' ? 'bg-warning-100 text-warning-800' :
                'bg-danger-100 text-danger-800'
              }`}>
                {formatPercentage(risk_percentages['1_month_risk'], 1)}
              </div>
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-1">
              1-Month Risk
            </h3>
            <p className="text-sm text-secondary-600">
              Short-term assessment
            </p>
          </div>
        </div>

        {/* 3-Month Risk */}
        <div className="card ring-2 ring-primary-200">
          <div className="card-body text-center">
            <div className="mb-4">
              <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold ${
                getRiskLevelColor(analysis.risk_level) === 'success' ? 'bg-success-100 text-success-800' :
                getRiskLevelColor(analysis.risk_level) === 'warning' ? 'bg-warning-100 text-warning-800' :
                'bg-danger-100 text-danger-800'
              }`}>
                {formatPercentage(risk_percentages['3_month_risk'], 1)}
              </div>
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-1">
              3-Month Risk
            </h3>
            <p className="text-sm text-secondary-600">
              Primary assessment period
            </p>
            <div className="mt-2">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                Main Focus
              </span>
            </div>
          </div>
        </div>

        {/* 6-Month Risk */}
        <div className="card">
          <div className="card-body text-center">
            <div className="mb-4">
              <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold ${
                getRiskLevelColor(analysis.risk_level) === 'success' ? 'bg-success-100 text-success-800' :
                getRiskLevelColor(analysis.risk_level) === 'warning' ? 'bg-warning-100 text-warning-800' :
                'bg-danger-100 text-danger-800'
              }`}>
                {formatPercentage(risk_percentages['6_month_risk'], 1)}
              </div>
            </div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-1">
              6-Month Risk
            </h3>
            <p className="text-sm text-secondary-600">
              Extended outlook
            </p>
            <div className="mt-2 flex items-center justify-center gap-1">
              <TrendIcon className={`w-3 h-3 ${
                riskTrend.color === 'success' ? 'text-success-600' :
                riskTrend.color === 'warning' ? 'text-warning-600' :
                'text-danger-600'
              }`} />
              <span className={`text-xs font-medium ${
                riskTrend.color === 'success' ? 'text-success-600' :
                riskTrend.color === 'warning' ? 'text-warning-600' :
                'text-danger-600'
              }`}>
                {riskTrend.trend}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Health Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {healthMetrics.map((metric, index) => (
          <div key={index} className="card">
            <div className="card-body">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium text-secondary-700">
                  {metric.label}
                </h4>
                <div className={`w-2 h-2 rounded-full ${
                  metric.type === 'low' ? 'bg-success-400' :
                  metric.type === 'moderate' ? 'bg-warning-400' :
                  metric.type === 'high' ? 'bg-danger-400' :
                  'bg-secondary-400'
                }`} />
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-bold text-secondary-900">
                  {metric.value}
                </span>
                {metric.unit && (
                  <span className="text-sm text-secondary-500">
                    {metric.unit}
                  </span>
                )}
              </div>
              {metric.description && (
                <p className="text-xs text-secondary-600 mt-1">
                  {metric.description}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Analysis Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Analysis */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-secondary-900 flex items-center gap-2">
              <Target className="w-5 h-5 text-secondary-600" />
              Risk Analysis
            </h3>
          </div>
          <div className="card-body space-y-4">
            <div className={`p-4 rounded-lg border ${
              riskColor === 'success' ? 'bg-success-50 border-success-200' :
              riskColor === 'warning' ? 'bg-warning-50 border-warning-200' :
              'bg-danger-50 border-danger-200'
            }`}>
              <div className="flex items-center gap-2 mb-2">
                {riskColor === 'success' ? (
                  <CheckCircle className="w-5 h-5 text-success-600" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-warning-600" />
                )}
                <span className="font-semibold">
                  Risk Level: {analysis.risk_level.replace('-', ' ').toUpperCase()}
                </span>
              </div>
              <p className="text-sm">
                Based on your age ({patient_data.age} years), BMI ({patient_data.bmi}), 
                and activity level ({analysis.activity_level}), your diabetes risk is 
                classified as {analysis.risk_level.replace('-', ' ')}.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-secondary-700 mb-1">
                  Baseline Risk
                </p>
                <p className="text-lg font-semibold text-secondary-900">
                  {formatPercentage(analysis.baseline_risk)}
                </p>
                <p className="text-xs text-secondary-600">
                  Age-adjusted baseline
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-secondary-700 mb-1">
                  Calculation Method
                </p>
                <p className="text-sm text-secondary-900">
                  {analysis.risk_calculation_method.replace('_', ' ').toLowerCase()}
                </p>
                <p className="text-xs text-secondary-600">
                  Method used for assessment
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Activity Analysis */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-secondary-900 flex items-center gap-2">
              <Activity className="w-5 h-5 text-secondary-600" />
              Activity Analysis
            </h3>
          </div>
          <div className="card-body space-y-4">
            <div className={`p-4 rounded-lg border ${
              activityLevel.level === 'high' ? 'bg-success-50 border-success-200' :
              activityLevel.level === 'moderate' ? 'bg-warning-50 border-warning-200' :
              'bg-danger-50 border-danger-200'
            }`}>
              <div className="flex items-center gap-2 mb-2">
                <Activity className={`w-5 h-5 ${
                  activityLevel.level === 'high' ? 'text-success-600' :
                  activityLevel.level === 'moderate' ? 'text-warning-600' :
                  'text-danger-600'
                }`} />
                <span className="font-semibold">
                  {activityLevel.level.toUpperCase()} Activity Level
                </span>
              </div>
              <p className="text-sm mb-3">
                {activityLevel.description}
              </p>
              <div className="space-y-1">
                {activityLevel.recommendations.slice(0, 2).map((rec, index) => (
                  <p key={index} className="text-xs flex items-start gap-1">
                    <span className="text-current">•</span>
                    <span>{rec}</span>
                  </p>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-secondary-700 mb-1">
                  Average Daily Steps
                </p>
                <p className="text-lg font-semibold text-secondary-900">
                  {formatNumber(analysis.avg_daily_steps)}
                </p>
                <p className="text-xs text-secondary-600">
                  Over {patient_data.step_count_days} days
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-secondary-700 mb-1">
                  Activity Category
                </p>
                <p className="text-sm text-secondary-900 capitalize">
                  {analysis.activity_level}
                </p>
                <p className="text-xs text-secondary-600">
                  Based on step count
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Data Summary */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-secondary-900 flex items-center gap-2">
            <User className="w-5 h-5 text-secondary-600" />
            Assessment Summary
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <h4 className="font-medium text-secondary-900">Patient Profile</h4>
              <div className="space-y-1 text-sm text-secondary-600">
                <p>Age: {patient_data.age} years</p>
                <p>BMI: {patient_data.bmi} kg/m²</p>
                <p>Data Period: {patient_data.step_count_days} days</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-secondary-900">Risk Forecast</h4>
              <div className="space-y-1 text-sm text-secondary-600">
                <p>1 Month: {formatPercentage(risk_percentages['1_month_risk'])}</p>
                <p>3 Months: {formatPercentage(risk_percentages['3_month_risk'])}</p>
                <p>6 Months: {formatPercentage(risk_percentages['6_month_risk'])}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-secondary-900">Key Insights</h4>
              <div className="space-y-1 text-sm text-secondary-600">
                <p>Risk Level: {analysis.risk_level.replace('-', ' ')}</p>
                <p>Activity: {analysis.activity_level}</p>
                <p>Method: {analysis.risk_calculation_method.replace('_', ' ')}</p>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-secondary-50 rounded-lg">
            <div className="flex items-start gap-2">
              <Info className="w-4 h-4 text-secondary-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-secondary-700">
                <p className="font-medium mb-1">About These Results</p>
                <p>
                  This assessment uses machine learning models trained on health data 
                  to estimate diabetes risk. Results are for informational purposes and 
                  should not replace professional medical advice. Consult your healthcare 
                  provider for personalized guidance.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard; 