# 🩺 DiabetaLens Frontend

Modern React application for AI-powered diabetes risk assessment with Claude AI recommendations.

## ✨ Features

- **🎯 Interactive Risk Assessment Form** - User-friendly input for age, BMI, and step data
- **📊 Beautiful Results Dashboard** - Comprehensive visualization of risk analysis
- **🤖 AI-Powered Recommendations** - Claude AI generates personalized health advice
- **📱 Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **⚡ Real-time API Integration** - Seamless connection to FastAPI backend
- **💾 Local Storage** - Automatically saves and restores user data
- **🎨 Modern UI** - Built with Tailwind CSS and Lucide icons

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks and functional components
- **TypeScript** - Full type safety and better developer experience
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework for styling
- **Lucide React** - Beautiful icons and graphics
- **Axios** - HTTP client for API communication
- **React Hook Form** - Form handling and validation
- **React Hot Toast** - Elegant toast notifications

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- DiabetaLens backend running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Environment Variables

Create a `.env` file in the frontend directory (optional):

```env
# Backend API URL (defaults to http://localhost:8000)
VITE_API_URL=http://localhost:8000
```

## 📖 Usage Guide

### 1. Risk Assessment Form

**Personal Information:**
- Age (18-100 years)
- Weight (kg)
- Height (cm) - automatically calculates BMI
- BMI is displayed with color-coded health categories

**Activity Data:**
- Enter daily step counts for past 28 days
- Supports multiple input formats:
  - `Day 1: 7500 steps`
  - `7500`
  - `Steps: 7500`
  - `2024-01-01: 7500`
- Minimum 14 days required for analysis
- Use "Fill Sample Data" for testing

### 2. Results Dashboard

**Risk Overview:**
- 1-month, 3-month, and 6-month risk percentages
- Color-coded risk levels (low, moderate, high)
- Risk trend analysis (increasing, stable, decreasing)

**Health Metrics:**
- Age, BMI, daily steps, diabetes risk
- Activity level analysis with recommendations
- Baseline risk and calculation method

**Analysis Summary:**
- Detailed breakdown of risk factors
- Activity level classification
- Key insights and methodology

### 3. AI Recommendations

**Comprehensive Recommendations:**
- Personalized health plan from Claude AI
- Activity and exercise tips
- Risk education and explanation
- Copy functionality for easy sharing

**Features:**
- Expandable sections for easy reading
- Token usage tracking
- Refresh capability for new recommendations
- Professional medical disclaimer

## 🎨 Design System

### Color Palette

```css
/* Primary - Blue theme for medical/health */
primary: #0ea5e9 (blue-500)

/* Success - Green for good health metrics */
success: #22c55e (green-500)

/* Warning - Orange for moderate risk */
warning: #f97316 (orange-500)

/* Danger - Red for high risk */
danger: #ef4444 (red-500)

/* Secondary - Gray for neutral elements */
secondary: #64748b (slate-500)
```

### Component Library

**Cards:**
- `.card` - Main container with shadow and border
- `.card-header` - Header section with background
- `.card-body` - Main content area
- `.card-footer` - Footer section

**Buttons:**
- `.btn-primary` - Main action buttons
- `.btn-secondary` - Secondary actions
- `.btn-success` - Positive actions
- `.btn-warning` - Warning actions
- `.btn-danger` - Destructive actions

**Health Metrics:**
- `.health-metric-low` - Good health indicators
- `.health-metric-moderate` - Warning indicators
- `.health-metric-high` - Risk indicators

## 🔗 API Integration

### Endpoints Used

```typescript
// Risk Assessment
POST /risk/assess - Calculate diabetes risk
GET /risk/baseline/{age} - Get baseline risk
POST /risk/activity/analyze - Analyze activity level

// Claude AI Recommendations
POST /recommendations/generate/comprehensive - Get all recommendation types
GET /recommendations/test-claude - Test Claude AI connection

// System
GET /health - API health check
GET / - Root endpoint
```

### Error Handling

- Network connection errors
- API endpoint not found (404)
- Server errors (500)
- Invalid data validation
- Toast notifications for user feedback

## 📱 Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Features:**
- Mobile-first design approach
- Touch-friendly interaction areas
- Optimized typography and spacing
- Adaptive grid layouts

## 🔧 Development

### Available Scripts

```bash
# Development server with hot reload
npm run dev

# Type checking
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── RiskAssessmentForm.tsx
│   │   ├── ResultsDashboard.tsx
│   │   └── RecommendationsDisplay.tsx
│   ├── services/           # API integration
│   │   └── api.ts
│   ├── types/              # TypeScript definitions
│   │   └── index.ts
│   ├── utils/              # Helper functions
│   │   └── index.ts
│   ├── App.tsx             # Main application
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json            # Dependencies
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS config
└── tsconfig.json           # TypeScript config
```

### Code Style

- **TypeScript strict mode** enabled
- **ESLint** for code quality
- **Prettier** for formatting (recommended)
- **Functional components** with hooks
- **Props interfaces** for all components

## 🧪 Testing

### Manual Testing Checklist

- [ ] Form validation works correctly
- [ ] BMI calculation updates automatically
- [ ] Step data parsing handles various formats
- [ ] API errors display helpful messages
- [ ] Results dashboard shows all metrics
- [ ] Recommendations display properly formatted
- [ ] Navigation between sections works
- [ ] Local storage saves/restores data
- [ ] Responsive design on mobile/tablet
- [ ] Toast notifications appear correctly

### Test Data

Use the "Fill Sample Data" button for quick testing:
- Age: 45 years
- Weight: 75 kg
- Height: 175 cm (BMI: 24.5)
- 28 days of sample step data (~7,000 steps/day)

## 🚀 Deployment

### Build for Production

```bash
# Create optimized build
npm run build

# Files will be in dist/ directory
# Serve with any static file server
```

### Deployment Options

**Static Hosting:**
- Vercel (recommended)
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

**Configuration:**
- Set `VITE_API_URL` to your production backend URL
- Ensure CORS is configured on backend
- Use HTTPS for production

## 🔒 Security & Privacy

- **No sensitive data storage** - Only stores assessment results locally
- **HTTPS required** for production deployment
- **API key protection** - Claude API key stored securely on backend
- **Input validation** - All user inputs validated client and server-side
- **Medical disclaimer** - Clear warnings about medical advice

## 🐛 Troubleshooting

### Common Issues

**API Connection Failed:**
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify network connectivity

**Build Errors:**
- Delete `node_modules` and reinstall
- Check Node.js version (18+ required)
- Verify all dependencies are installed

**TypeScript Errors:**
- Run `npm run type-check`
- Check import paths
- Ensure all props have proper types

## 🤝 Contributing

1. Follow existing code style and patterns
2. Add TypeScript types for all new components
3. Test responsiveness on different screen sizes
4. Ensure accessibility compliance
5. Update documentation for new features

## 📄 License

Part of the DiabetaLens project. See main project README for license details.

---

**Frontend Status: Complete ✅**  
*Ready for production deployment and user testing* 