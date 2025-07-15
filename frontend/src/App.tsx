import React, { useState, useEffect } from 'react';
import { toast, Toaster } from 'react-hot-toast';
import { 
  Heart, 
  Activity, 
  Brain,
  Stethoscope,
  Github,
  ExternalLink,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

import RiskAssessmentForm from './components/RiskAssessmentForm';
import ResultsDashboard from './components/ResultsDashboard';
import RecommendationsDisplay from './components/RecommendationsDisplay';

import { apiService } from './services/api';
import { 
  RiskAssessmentRequest, 
  RiskAssessmentResult, 
  ComprehensiveRecommendations,
  LoadingState 
} from './types';
import { saveToLocalStorage, loadFromLocalStorage } from './utils';

const App: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'form' | 'results' | 'recommendations'>('form');
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  
  const [riskResults, setRiskResults] = useState<RiskAssessmentResult | null>(
    loadFromLocalStorage('diabetalens_risk_results', null)
  );
  const [recommendations, setRecommendations] = useState<ComprehensiveRecommendations | null>(
    loadFromLocalStorage('diabetalens_recommendations', null)
  );
  
  const [loading, setLoading] = useState<LoadingState>({ isLoading: false });
  const [recommendationsLoading, setRecommendationsLoading] = useState<LoadingState>({ isLoading: false });

  // Check API status on mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  // Auto-save results to localStorage
  useEffect(() => {
    if (riskResults) {
      saveToLocalStorage('diabetalens_risk_results', riskResults);
    }
  }, [riskResults]);

  useEffect(() => {
    if (recommendations) {
      saveToLocalStorage('diabetalens_recommendations', recommendations);
    }
  }, [recommendations]);

  const checkApiStatus = async () => {
    try {
      const result = await apiService.healthCheck();
      if (result.status === 'success') {
        setApiStatus('online');
        toast.success('Connected to DiabetaLens API');
      } else {
        setApiStatus('offline');
        toast.error('API is offline. Please start the backend server.');
      }
    } catch (error) {
      setApiStatus('offline');
      toast.error('Cannot connect to backend. Make sure it\'s running on port 8000.');
    }
  };

  const handleRiskAssessment = async (data: RiskAssessmentRequest) => {
    setLoading({ 
      isLoading: true, 
      message: 'Calculating diabetes risk using ML models...' 
    });

    try {
      // Perform risk assessment
      const results = await apiService.assessRisk(data);
      setRiskResults(results);
      
      toast.success('Risk assessment completed successfully!');
      setCurrentStep('results');
      
      // Automatically generate AI recommendations
      setTimeout(() => {
        generateRecommendations(results);
      }, 1000);
      
    } catch (error) {
      console.error('Risk assessment failed:', error);
      toast.error(
        error instanceof Error 
          ? error.message 
          : 'Failed to calculate risk. Please try again.'
      );
    } finally {
      setLoading({ isLoading: false });
    }
  };

  const generateRecommendations = async (results?: RiskAssessmentResult) => {
    const riskData = results || riskResults;
    if (!riskData) {
      toast.error('No risk assessment data available. Please complete an assessment first.');
      return;
    }

    setRecommendationsLoading({ 
      isLoading: true, 
      message: 'Generating AI recommendations with Claude...' 
    });

    try {
      const requestData = {
        user_profile: {
          age: riskData.patient_data.age,
          bmi: riskData.patient_data.bmi,
          activity_level: riskData.analysis.activity_level,
          avg_daily_steps: riskData.analysis.avg_daily_steps
        },
        risk_data: riskData
      };

      const recommendations = await apiService.getComprehensiveRecommendations(requestData);
      setRecommendations(recommendations);
      
      toast.success('AI recommendations generated successfully!');
      setCurrentStep('recommendations');
      
    } catch (error) {
      console.error('Recommendations generation failed:', error);
      toast.error(
        error instanceof Error 
          ? error.message 
          : 'Failed to generate recommendations. Please try again.'
      );
    } finally {
      setRecommendationsLoading({ isLoading: false });
    }
  };

  const handleNewAssessment = () => {
    setCurrentStep('form');
    setRiskResults(null);
    setRecommendations(null);
    // Clear localStorage
    localStorage.removeItem('diabetalens_risk_results');
    localStorage.removeItem('diabetalens_recommendations');
    toast.success('Ready for new assessment');
  };

  const handleViewResults = () => {
    if (riskResults) {
      setCurrentStep('results');
    }
  };

  const handleViewRecommendations = () => {
    if (recommendations) {
      setCurrentStep('recommendations');
    } else if (riskResults) {
      generateRecommendations();
    }
  };

  return (
    <div className="min-h-screen bg-secondary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="p-2 bg-primary-100 rounded-lg">
                  <Stethoscope className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-secondary-900">
                    DiabetaLens
                  </h1>
                  <p className="text-xs text-secondary-600">
                    AI-Powered Health Analytics
                  </p>
                </div>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center gap-4">
              {riskResults && (
                <button
                  onClick={handleViewResults}
                  className={`btn btn-secondary text-sm ${
                    currentStep === 'results' ? 'ring-2 ring-primary-200' : ''
                  }`}
                >
                  <Activity className="w-4 h-4 mr-1" />
                  Results
                </button>
              )}
              
              {(recommendations || riskResults) && (
                <button
                  onClick={handleViewRecommendations}
                  className={`btn btn-secondary text-sm ${
                    currentStep === 'recommendations' ? 'ring-2 ring-primary-200' : ''
                  }`}
                  disabled={recommendationsLoading.isLoading}
                >
                  <Brain className="w-4 h-4 mr-1" />
                  AI Recommendations
                </button>
              )}

              <button
                onClick={handleNewAssessment}
                className="btn btn-primary text-sm"
              >
                <Heart className="w-4 h-4 mr-1" />
                New Assessment
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* API Status Indicator */}
      <div className="bg-secondary-100 border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              {apiStatus === 'checking' && (
                <>
                  <div className="animate-spin rounded-full h-3 w-3 border-b border-secondary-600"></div>
                  <span className="text-secondary-600">Checking API status...</span>
                </>
              )}
              {apiStatus === 'online' && (
                <>
                  <CheckCircle className="w-3 h-3 text-success-600" />
                  <span className="text-success-700">Backend API Connected</span>
                </>
              )}
              {apiStatus === 'offline' && (
                <>
                  <AlertCircle className="w-3 h-3 text-danger-600" />
                  <span className="text-danger-700">Backend API Offline</span>
                  <button
                    onClick={checkApiStatus}
                    className="ml-2 text-primary-600 hover:text-primary-800 underline"
                  >
                    Retry
                  </button>
                </>
              )}
            </div>

            <div className="flex items-center gap-4 text-secondary-600">
              <span>v1.0.0</span>
              <a
                href="https://github.com/diabetalens"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 hover:text-primary-600 transition-colors"
              >
                <Github className="w-3 h-3" />
                GitHub
                <ExternalLink className="w-2 h-2" />
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="py-8">
        {currentStep === 'form' && (
          <RiskAssessmentForm
            onSubmit={handleRiskAssessment}
            loading={loading}
          />
        )}

        {currentStep === 'results' && riskResults && (
          <ResultsDashboard
            results={riskResults}
            onNewAssessment={handleNewAssessment}
          />
        )}

        {currentStep === 'recommendations' && (
          <RecommendationsDisplay
            recommendations={recommendations}
            loading={recommendationsLoading}
            onRefresh={() => generateRecommendations()}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-secondary-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Stethoscope className="w-5 h-5 text-primary-600" />
                <span className="font-semibold text-secondary-900">DiabetaLens</span>
              </div>
              <p className="text-sm text-secondary-600 leading-relaxed">
                AI-powered diabetes risk assessment system using machine learning 
                and Claude AI to provide personalized health insights and recommendations.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-secondary-900 mb-4">Features</h3>
              <ul className="space-y-2 text-sm text-secondary-600">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3 text-success-600" />
                  ML-powered risk calculation
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3 text-success-600" />
                  Claude AI recommendations
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3 text-success-600" />
                  Activity level analysis
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3 text-success-600" />
                  Personalized health insights
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-secondary-900 mb-4">Important Notice</h3>
              <p className="text-sm text-secondary-600 leading-relaxed">
                This tool is for informational purposes only and should not replace 
                professional medical advice. Always consult healthcare providers for 
                medical decisions.
              </p>
            </div>
          </div>

          <div className="border-t border-secondary-200 mt-8 pt-6">
            <div className="flex items-center justify-between text-sm text-secondary-600">
              <p>© 2024 DiabetaLens. Built with React, FastAPI, and Claude AI.</p>
              <p>
                Phase 3: Frontend Development Complete ✅
              </p>
            </div>
          </div>
        </div>
      </footer>

      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#fff',
            color: '#374151',
            border: '1px solid #e5e7eb',
            borderRadius: '0.75rem',
            fontSize: '0.875rem',
          },
          success: {
            iconTheme: {
              primary: '#22c55e',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
};

export default App; 