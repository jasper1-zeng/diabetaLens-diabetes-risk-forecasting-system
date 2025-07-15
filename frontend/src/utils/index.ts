import { BMICategory, HealthMetric, ActivityLevel } from '../types';

// BMI Calculation and Classification
export function calculateBMI(weight: number, height: number): number {
  if (weight <= 0 || height <= 0) return 0;
  return Number((weight / Math.pow(height / 100, 2)).toFixed(1));
}

export function getBMICategory(bmi: number): BMICategory {
  if (bmi < 18.5) {
    return {
      category: 'underweight',
      range: '< 18.5',
      color: 'warning'
    };
  } else if (bmi < 25) {
    return {
      category: 'normal',
      range: '18.5 - 24.9',
      color: 'success'
    };
  } else if (bmi < 30) {
    return {
      category: 'overweight',
      range: '25.0 - 29.9',
      color: 'warning'
    };
  } else {
    return {
      category: 'obese',
      range: '≥ 30.0',
      color: 'danger'
    };
  }
}

// Activity Level Assessment
export function getActivityLevel(avgSteps: number): ActivityLevel {
  if (avgSteps < 5000) {
    return {
      level: 'low',
      description: 'Sedentary - Below recommended activity level',
      recommendations: [
        'Start with short 5-10 minute walks',
        'Take stairs instead of elevators',
        'Set hourly movement reminders',
        'Aim for 7,500 steps as next goal'
      ]
    };
  } else if (avgSteps < 8000) {
    return {
      level: 'moderate',
      description: 'Moderately active - Good baseline activity',
      recommendations: [
        'Increase to 8,000+ steps daily',
        'Add 2-3 strength training sessions',
        'Include 150+ minutes moderate exercise weekly',
        'Try interval walking or jogging'
      ]
    };
  } else {
    return {
      level: 'high',
      description: 'Highly active - Excellent activity level',
      recommendations: [
        'Maintain current activity level',
        'Add variety with different exercises',
        'Include strength and flexibility training',
        'Consider training for fitness goals'
      ]
    };
  }
}

// Risk Level Formatting
export function getRiskLevel(percentage: number): 'low' | 'moderate' | 'high' {
  if (percentage < 5) return 'low';
  if (percentage < 10) return 'moderate';
  return 'high';
}

export function getRiskLevelColor(level: string): string {
  switch (level.toLowerCase()) {
    case 'low-risk':
    case 'low':
      return 'success';
    case 'medium-risk':
    case 'moderate':
      return 'warning';
    case 'high-risk':
    case 'high':
      return 'danger';
    default:
      return 'secondary';
  }
}

// Number Formatting
export function formatPercentage(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`;
}

export function formatNumber(value: number, decimals: number = 0): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function formatSteps(steps: number): string {
  if (steps >= 1000) {
    return `${(steps / 1000).toFixed(1)}k`;
  }
  return steps.toString();
}

// Date Formatting
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function formatTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

// Validation Functions
export function validateAge(age: number): boolean {
  return age >= 18 && age <= 100;
}

export function validateBMI(bmi: number): boolean {
  return bmi >= 10 && bmi <= 60;
}

export function validateSteps(steps: number): boolean {
  return steps >= 0 && steps <= 50000;
}

export function validateStepData(stepData: number[]): boolean {
  return stepData.length === 28 && stepData.every(validateSteps);
}

// Step Data Processing
export function parseStepData(input: string): number[] {
  try {
    const lines = input.trim().split('\n');
    const steps: number[] = [];
    
    console.log('🔍 Parsing step data from input:', input.substring(0, 200) + '...');
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed === '') continue;
      
      // Try to extract step count from various formats
      let stepCount: number | null = null;
      
      // Format: "Day 1: 6500 steps" or "Day 1: 6500"
      const dayFormatMatch = trimmed.match(/Day\s+\d+:\s*(\d{3,})/i);
      if (dayFormatMatch) {
        stepCount = parseInt(dayFormatMatch[1]);
      }
      // Format: "6500 steps" or "6500"
      else if (trimmed.match(/^\d+(\s+steps?)?$/i)) {
        const numberMatch = trimmed.match(/^(\d+)/);
        if (numberMatch) {
          stepCount = parseInt(numberMatch[1]);
        }
      }
      // Format: standalone numbers (must be 3+ digits to avoid day numbers)
      else if (trimmed.match(/^\d{3,}$/)) {
        stepCount = parseInt(trimmed);
      }
      // Format: numbers in text (look for 3+ digit numbers, not day numbers)
      else {
        const numberMatch = trimmed.match(/\b(\d{3,})\b/);
        if (numberMatch) {
          stepCount = parseInt(numberMatch[1]);
        }
      }
      
      if (stepCount !== null && validateSteps(stepCount)) {
        steps.push(stepCount);
      }
    }
    
    console.log('📊 Parsed step data result:', steps.slice(0, 5), `(${steps.length} total)`);
    return steps;
  } catch (error) {
    console.error('Error parsing step data:', error);
    return [];
  }
}

export function generateSampleStepData(avgSteps: number = 7000, variance: number = 2000): number[] {
  const data: number[] = [];
  for (let i = 0; i < 28; i++) {
    const randomVariance = (Math.random() - 0.5) * variance;
    const steps = Math.max(0, Math.round(avgSteps + randomVariance));
    data.push(steps);
  }
  return data;
}

// Health Metrics Creation
export function createHealthMetrics(
  age: number,
  bmi: number,
  avgSteps: number,
  riskPercentage: number
): HealthMetric[] {
  const bmiCategory = getBMICategory(bmi);
  const activityLevel = getActivityLevel(avgSteps);
  const riskLevel = getRiskLevel(riskPercentage);

  return [
    {
      label: 'Age',
      value: age,
      unit: 'years',
      type: 'neutral',
      description: 'Your current age'
    },
    {
      label: 'BMI',
      value: bmi,
      unit: 'kg/m²',
      type: bmiCategory.color === 'success' ? 'low' : bmiCategory.color === 'warning' ? 'moderate' : 'high',
      description: `${bmiCategory.category} (${bmiCategory.range})`
    },
    {
      label: 'Daily Steps',
      value: formatNumber(avgSteps),
      unit: 'avg',
      type: activityLevel.level === 'high' ? 'low' : activityLevel.level === 'moderate' ? 'moderate' : 'high',
      description: activityLevel.description
    },
    {
      label: 'Diabetes Risk',
      value: formatPercentage(riskPercentage),
      unit: '3-month',
      type: riskLevel,
      description: `${riskLevel} risk level`
    }
  ];
}

// Text Processing
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}

export function capitalizeFirst(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

// CSS Class Helpers
export function cn(...classes: (string | undefined | null | boolean)[]): string {
  return classes.filter(Boolean).join(' ');
}

// Local Storage Helpers
export function saveToLocalStorage(key: string, data: any): void {
  try {
    localStorage.setItem(key, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving to localStorage:', error);
  }
}

export function loadFromLocalStorage<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Error loading from localStorage:', error);
    return defaultValue;
  }
}

// Async Utilities
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
} 