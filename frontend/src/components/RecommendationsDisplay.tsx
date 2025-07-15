import React, { useState } from 'react';
import { 
  Brain, 
  Heart, 
  Activity, 
  Lightbulb, 
  ChevronDown, 
  ChevronUp,
  Clock,
  Sparkles,
  Target,
  TrendingUp,
  MessageSquare,
  Copy,
  Check,
  RefreshCw
} from 'lucide-react';

import { 
  RecommendationResponse, 
  ComprehensiveRecommendations, 
  LoadingState 
} from '../types';
import { formatDate, formatTime, truncateText } from '../utils';

interface RecommendationsDisplayProps {
  recommendations?: RecommendationResponse | ComprehensiveRecommendations;
  loading: LoadingState;
  onRefresh?: () => void;
}

interface RecommendationSectionProps {
  title: string;
  content: string;
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning' | 'secondary';
  isExpanded?: boolean;
  onToggle?: () => void;
}

const RecommendationSection: React.FC<RecommendationSectionProps> = ({
  title,
  content,
  icon,
  color,
  isExpanded = true,
  onToggle
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy text:', error);
    }
  };

  const colorClasses = {
    primary: {
      bg: 'bg-primary-50',
      border: 'border-primary-200',
      icon: 'text-primary-600',
      header: 'bg-primary-100'
    },
    success: {
      bg: 'bg-success-50',
      border: 'border-success-200',
      icon: 'text-success-600',
      header: 'bg-success-100'
    },
    warning: {
      bg: 'bg-warning-50',
      border: 'border-warning-200',
      icon: 'text-warning-600',
      header: 'bg-warning-100'
    },
    secondary: {
      bg: 'bg-secondary-50',
      border: 'border-secondary-200',
      icon: 'text-secondary-600',
      header: 'bg-secondary-100'
    }
  };

  const classes = colorClasses[color];

  return (
    <div className={`border rounded-lg overflow-hidden ${classes.bg} ${classes.border}`}>
      <div 
        className={`px-4 py-3 ${classes.header} ${onToggle ? 'cursor-pointer' : ''}`}
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`${classes.icon}`}>
              {icon}
            </div>
            <h3 className="font-semibold text-secondary-900">
              {title}
            </h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleCopy();
              }}
              className="p-1 hover:bg-white/50 rounded transition-colors"
              title="Copy content"
            >
              {copied ? (
                <Check className="w-4 h-4 text-success-600" />
              ) : (
                <Copy className="w-4 h-4 text-secondary-600" />
              )}
            </button>
            {onToggle && (
              <div className="text-secondary-600">
                {isExpanded ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      
      {isExpanded && (
        <div className="px-4 py-4">
          <div className="prose prose-sm max-w-none">
            {content.split('\n').map((paragraph, index) => {
              if (paragraph.trim() === '') return null;
              
              // Handle markdown-style formatting
              if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                return (
                  <h4 key={index} className="font-semibold text-secondary-900 mt-4 mb-2">
                    {paragraph.slice(2, -2)}
                  </h4>
                );
              }
              
              if (paragraph.startsWith('• ') || paragraph.startsWith('- ')) {
                return (
                  <div key={index} className="flex items-start gap-2 mb-2">
                    <span className="text-current mt-1">•</span>
                    <span className="text-secondary-700">{paragraph.slice(2)}</span>
                  </div>
                );
              }
              
              if (paragraph.includes('🎯') || paragraph.includes('📈') || paragraph.includes('💡')) {
                return (
                  <p key={index} className="font-medium text-secondary-900 mb-3">
                    {paragraph}
                  </p>
                );
              }
              
              return (
                <p key={index} className="text-secondary-700 mb-3 leading-relaxed">
                  {paragraph}
                </p>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

const RecommendationsDisplay: React.FC<RecommendationsDisplayProps> = ({
  recommendations,
  loading,
  onRefresh
}) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(['comprehensive']) // Start with comprehensive expanded
  );

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId);
      } else {
        newSet.add(sectionId);
      }
      return newSet;
    });
  };

  if (loading.isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="card">
          <div className="card-body text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">
              Generating AI Recommendations
            </h3>
            <p className="text-secondary-600">
              {loading.message || 'Claude AI is analyzing your health data and creating personalized recommendations...'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!recommendations) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="card">
          <div className="card-body text-center py-12">
            <Brain className="w-12 h-12 text-secondary-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">
              No Recommendations Available
            </h3>
            <p className="text-secondary-600">
              Complete a risk assessment to receive AI-powered health recommendations.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Check if this is comprehensive recommendations or single recommendation
  const isComprehensive = 'recommendations' in recommendations && recommendations.recommendations && 'comprehensive' in recommendations.recommendations;

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-100 rounded-lg">
                <Brain className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-secondary-900 flex items-center gap-2">
                  AI Health Recommendations
                  <Sparkles className="w-5 h-5 text-primary-600" />
                </h2>
                <p className="text-sm text-secondary-600 flex items-center gap-2">
                  <Clock className="w-3 h-3" />
                  Generated by Claude AI • {formatDate(
                    isComprehensive 
                                        ? recommendations.metadata.generated_at
                  : recommendations.timestamp
                )} at {formatTime(
                  isComprehensive 
                  ? recommendations.metadata.generated_at
                  : recommendations.timestamp
                  )}
                </p>
              </div>
            </div>
            
            {onRefresh && (
              <button
                onClick={onRefresh}
                className="btn btn-secondary"
                title="Generate new recommendations"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations Content */}
      {isComprehensive ? (
        <div className="space-y-4">
          {/* Summary Card */}
          <div className="card">
            <div className="card-body">
              <div className="flex items-center gap-2 mb-3">
                <MessageSquare className="w-5 h-5 text-secondary-600" />
                <h3 className="font-semibold text-secondary-900">Summary</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-secondary-700">API Calls:</span>
                  <span className="text-secondary-900">3 recommendations</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-secondary-700">Types:</span>
                  <span className="text-secondary-900">3 types</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-secondary-700">Model:</span>
                  <span className="text-secondary-900">{recommendations.metadata.model_used}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Comprehensive Recommendations */}
          <RecommendationSection
            title="Comprehensive Health Plan"
            content={recommendations.recommendations.comprehensive.content}
            icon={<Heart className="w-5 h-5" />}
            color="primary"
            isExpanded={expandedSections.has('comprehensive')}
            onToggle={() => toggleSection('comprehensive')}
          />

          {/* Activity-Focused Recommendations */}
          <RecommendationSection
            title="Activity & Exercise Tips"
            content={recommendations.recommendations.activity_focused.content}
            icon={<Activity className="w-5 h-5" />}
            color="success"
            isExpanded={expandedSections.has('activity')}
            onToggle={() => toggleSection('activity')}
          />

          {/* Risk Explanation */}
          <RecommendationSection
            title="Understanding Your Risk"
            content={recommendations.recommendations.risk_explanation.content}
            icon={<Target className="w-5 h-5" />}
            color="warning"
            isExpanded={expandedSections.has('risk')}
            onToggle={() => toggleSection('risk')}
          />

          {/* Token Usage Info */}
          {recommendations.metadata.api_usage && (
            <div className="card">
              <div className="card-body">
                <div className="flex items-center gap-2 mb-3">
                  <TrendingUp className="w-5 h-5 text-secondary-600" />
                  <h3 className="font-semibold text-secondary-900">API Usage Details</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-secondary-700">Input Tokens:</span>
                    <span className="text-secondary-900">
                      {recommendations.metadata.api_usage.total_input_tokens.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-secondary-700">Output Tokens:</span>
                    <span className="text-secondary-900">
                      {recommendations.metadata.api_usage.total_output_tokens.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {/* Single Recommendation */}
          <RecommendationSection
            title="Personalized Health Recommendations"
            content={recommendations.recommendations}
            icon={<Lightbulb className="w-5 h-5" />}
            color="primary"
            isExpanded={true}
          />

          {/* Metadata */}
          <div className="card">
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-secondary-700">Model Used:</span>
                  <span className="text-secondary-900">{recommendations.model_used}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-secondary-700">Generated:</span>
                  <span className="text-secondary-900">
                    {formatDate(recommendations.timestamp)} {formatTime(recommendations.timestamp)}
                  </span>
                </div>
                {recommendations.token_usage && (
                  <>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-secondary-700">Input Tokens:</span>
                      <span className="text-secondary-900">
                        {recommendations.token_usage.input_tokens.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-secondary-700">Output Tokens:</span>
                      <span className="text-secondary-900">
                        {recommendations.token_usage.output_tokens.toLocaleString()}
                      </span>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <div className="card">
        <div className="card-body">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-secondary-100 rounded-lg flex-shrink-0">
              <Brain className="w-4 h-4 text-secondary-600" />
            </div>
            <div className="text-sm text-secondary-700">
              <p className="font-medium mb-2">AI-Generated Health Recommendations</p>
              <p className="leading-relaxed">
                These recommendations are generated by Claude AI based on your risk assessment data. 
                They are for informational purposes only and should not replace professional medical advice. 
                Always consult with qualified healthcare providers before making significant changes to your 
                health, diet, or exercise routines.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsDisplay; 