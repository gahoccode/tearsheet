'use client';

import { useState } from 'react';
import PortfolioForm from '@/components/PortfolioForm';
import QuantStatsTearsheet from '@/components/QuantStatsTearsheet';

interface TearsheetResponse {
  html: string;
  portfolio_name: string;
  symbols: string[];
  period: string;
  data_points: number;
}

export default function HomePage() {
  const [tearsheetData, setTearsheetData] = useState<TearsheetResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalysisComplete = (data: TearsheetResponse) => {
    setTearsheetData(data);
    setIsAnalyzing(false);
  };

  const handleNewAnalysis = () => {
    setTearsheetData(null);
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!tearsheetData ? (
          // Portfolio Input Form
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Portfolio Analysis Tool
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Analyze your Vietnamese stock portfolio with comprehensive QuantStats tearsheet 
                featuring professional performance metrics and risk assessment.
              </p>
            </div>
            <PortfolioForm onAnalysisComplete={handleAnalysisComplete} />
          </div>
        ) : (
          // QuantStats Tearsheet
          <QuantStatsTearsheet
            htmlContent={tearsheetData.html}
            portfolioName={tearsheetData.portfolio_name}
            symbols={tearsheetData.symbols}
            period={tearsheetData.period}
            dataPoints={tearsheetData.data_points}
            onNewAnalysis={handleNewAnalysis}
          />
        )}
      </div>
    </div>
  );
}
