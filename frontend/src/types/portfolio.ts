// TypeScript types for portfolio analysis

export interface Stock {
  symbol: string;
  weight: number;
  name?: string;
  sector?: string;
  allocation?: number;
}

export interface Portfolio {
  name?: string;
  capital: number;
  start_date: string;
  end_date: string;
  created_at: string;
  stocks: Stock[];
  summary: {
    size: number;
    total_weight: number;
    symbols: string[];
  };
}

export interface PerformanceMetrics {
  total_return: number;
  annualized_return: number;
  volatility: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_periods: number;
  start_date: string;
  end_date: string;
}

export interface ReturnsData {
  data: Record<string, number>;
  dates: string[];
  values: number[];
}

export interface AnalysisSummary {
  data_points: number;
  period: {
    start: string;
    end: string;
    days: number;
  };
  portfolio_size: number;
  total_capital: number;
}

export interface PlotlyChartData {
  data: any[];
  layout: any;
}

export interface PlotlyCharts {
  performance: PlotlyChartData;
  drawdown: PlotlyChartData;
  composition: PlotlyChartData;
  metrics_dashboard: PlotlyChartData;
}

export interface PortfolioAnalysisResponse {
  portfolio: Portfolio;
  metrics: PerformanceMetrics;
  returns: ReturnsData;
  charts: PlotlyCharts;
  analysis_summary: AnalysisSummary;
}

export interface PortfolioFormData {
  symbols: string[];
  weights: number[];
  capital: number;
  start_date: string;
  end_date: string;
  name?: string;
}

export interface ValidationResponse {
  valid: boolean;
  error?: string;
  validated_data?: {
    symbols: string[];
    weights: number[];
    capital: number;
    start_date: string;
    end_date: string;
    validation_timestamp: string;
  };
}

// Financial ratios types
export interface RatioData {
  symbol: string;
  data: Record<string, any>[];
  columns: string[];
  index: string[];
}

export interface SummaryData {
  symbol: string;
  pe_ratio?: number;
  pb_ratio?: number;
  roe?: number;
  roa?: number;
}

export interface RatiosAnalysisResponse {
  symbols: string[];
  period: string;
  ratio_data: Record<string, RatioData>;
  summary_data: SummaryData[];
}

export interface ApiError {
  error: string;
}

// Form validation types
export interface PortfolioFormErrors {
  symbols?: string;
  weights?: string;
  capital?: string;
  start_date?: string;
  end_date?: string;
  general?: string;
}