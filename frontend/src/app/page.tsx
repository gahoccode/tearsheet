'use client';

import { useState } from 'react';
import PortfolioForm from '@/components/PortfolioForm';
import MetricsDashboard from '@/components/MetricsDashboard';
import PerformanceChart from '@/components/charts/PerformanceChart';
import DrawdownChart from '@/components/charts/DrawdownChart';
import CompositionChart from '@/components/charts/CompositionChart';
import { PortfolioAnalysisResponse } from '@/types/portfolio';

export default function HomePage() {
  const [analysisData, setAnalysisData] = useState<PortfolioAnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalysisComplete = (data: PortfolioAnalysisResponse) => {
    setAnalysisData(data);
    setIsAnalyzing(false);
  };

  const handleNewAnalysis = () => {
    setAnalysisData(null);
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisData ? (
          // Portfolio Input Form
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Portfolio Analysis Tool
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Analyze your Vietnamese stock portfolio with comprehensive performance metrics, 
                interactive charts, and risk assessment tools.
              </p>
            </div>
            <PortfolioForm onAnalysisComplete={handleAnalysisComplete} />
          </div>
        ) : (
          // Analysis Results
          <div className="space-y-8">
            {/* Header with portfolio info and reset button */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    {analysisData.portfolio.name || 'Portfolio Analysis Results'}
                  </h1>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
                    <span>
                      <strong>Symbols:</strong> {analysisData.portfolio.summary.symbols.join(', ')}
                    </span>
                    <span>
                      <strong>Period:</strong> {analysisData.portfolio.start_date} to {analysisData.portfolio.end_date}
                    </span>
                    <span>
                      <strong>Capital:</strong> {analysisData.portfolio.capital.toLocaleString()} VND
                    </span>
                    <span>
                      <strong>Data Points:</strong> {analysisData.analysis_summary.data_points}
                    </span>
                  </div>
                </div>
                <button
                  onClick={handleNewAnalysis}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  New Analysis
                </button>
              </div>
            </div>

            {/* Portfolio Composition */}
            <CompositionChart 
              stocks={analysisData.portfolio.stocks} 
              capital={analysisData.portfolio.capital}
            />

            {/* Performance Metrics Dashboard */}
            <MetricsDashboard metrics={analysisData.metrics} />

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <PerformanceChart 
                returns={analysisData.returns} 
                title="Portfolio Performance Over Time"
              />
              <DrawdownChart 
                returns={analysisData.returns} 
                title="Portfolio Drawdown Analysis"
              />
            </div>

            {/* Additional Analysis Information */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600 mb-1">
                    {analysisData.analysis_summary.portfolio_size}
                  </div>
                  <div className="text-sm text-gray-600">Stocks in Portfolio</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600 mb-1">
                    {analysisData.analysis_summary.data_points}
                  </div>
                  <div className="text-sm text-gray-600">Trading Days Analyzed</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 mb-1">
                    {analysisData.analysis_summary.period.days}
                  </div>
                  <div className="text-sm text-gray-600">Calendar Days</div>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-900 mb-2">Data Information</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li><strong>Data Source:</strong> vnstock API (Vietnam stock market data)</li>
                  <li><strong>Analysis Method:</strong> Portfolio returns calculated using weighted average of individual stock returns</li>
                  <li><strong>Risk Metrics:</strong> Calculated based on daily return volatility and drawdown analysis</li>
                  <li><strong>Currency:</strong> Vietnamese Dong (VND)</li>
                  <li><strong>Charts:</strong> Interactive visualizations built with Recharts</li>
                </ul>
              </div>
            </div>

            {/* Export/Actions Section */}
            <div className="bg-blue-50 rounded-lg p-6 text-center">
              <h3 className="text-lg font-medium text-blue-900 mb-2">
                Analysis Complete
              </h3>
              <p className="text-blue-700 mb-4">
                Your portfolio analysis is ready. All charts are interactive - hover for details, 
                click and drag to zoom, and use the legend to toggle data series.
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleNewAnalysis}
                  className="px-6 py-2 bg-white text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Analyze Different Portfolio
                </button>
                <a
                  href="/ratios"
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  View Financial Ratios
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
