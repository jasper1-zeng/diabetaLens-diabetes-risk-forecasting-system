import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  RiskAssessmentRequest, 
  RiskAssessmentResult, 
  RecommendationRequest, 
  RecommendationResponse, 
  ComprehensiveRecommendations,
  ApiResponse 
} from '../types';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('❌ Response error:', error.response?.data || error.message);
        
        // Handle specific error cases
        if (error.response?.status === 404) {
          throw new Error('API endpoint not found. Make sure the backend is running.');
        } else if (error.response?.status === 500) {
          throw new Error('Internal server error. Please try again later.');
        } else if (error.code === 'ECONNREFUSED') {
          throw new Error('Unable to connect to server. Make sure the backend is running on port 8000.');
        }
        
        throw error;
      }
    );
  }

  // Health Check
  async healthCheck(): Promise<ApiResponse<{ status: string; message: string }>> {
    try {
      const response = await this.client.get('/health');
      return {
        status: 'success',
        data: response.data,
      };
    } catch (error) {
      return {
        status: 'error',
        message: error instanceof Error ? error.message : 'Health check failed',
      };
    }
  }

  // Risk Assessment Endpoints
  async assessRisk(data: RiskAssessmentRequest): Promise<RiskAssessmentResult> {
    const response = await this.client.post('/risk/assess', data);
    return response.data;
  }

  async getBaselineRisk(age: number): Promise<{ baseline_risk: number; age_group: string }> {
    const response = await this.client.get(`/risk/baseline/${age}`);
    return response.data;
  }

  async analyzeActivity(stepData: number[]): Promise<{
    activity_level: string;
    avg_daily_steps: number;
    analysis: string;
  }> {
    const response = await this.client.post('/risk/activity/analyze', {
      past_28_day_steps: stepData
    });
    return response.data;
  }

  // Claude AI Recommendation Endpoints
  async getRecommendations(data: RecommendationRequest): Promise<RecommendationResponse> {
    const response = await this.client.post('/recommendations/generate', data);
    return response.data;
  }

  async getComprehensiveRecommendations(data: RecommendationRequest): Promise<ComprehensiveRecommendations> {
    const response = await this.client.post('/recommendations/generate/comprehensive', data);
    return response.data;
  }

  async getActivityTips(data: RecommendationRequest): Promise<RecommendationResponse> {
    const response = await this.client.post('/recommendations/activity-tips', data);
    return response.data;
  }

  async getRiskExplanation(data: RecommendationRequest): Promise<RecommendationResponse> {
    const response = await this.client.post('/recommendations/risk-explanation', data);
    return response.data;
  }

  // Test Claude AI Connection
  async testClaudeConnection(): Promise<{ status: string; message: string; model?: string }> {
    const response = await this.client.get('/recommendations/test-claude');
    return response.data;
  }

  // Utility Methods
  async ping(): Promise<boolean> {
    try {
      const response = await this.client.get('/');
      return response.status === 200;
    } catch {
      return false;
    }
  }

  // Get detailed API metrics (if available)
  async getMetrics(): Promise<any> {
    try {
      const response = await this.client.get('/risk/metrics');
      return response.data;
    } catch (error) {
      console.warn('Metrics endpoint not available:', error);
      return null;
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export for testing or direct instantiation
export default ApiService; 