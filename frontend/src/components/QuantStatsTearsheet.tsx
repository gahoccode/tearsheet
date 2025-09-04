'use client';

interface QuantStatsTearsheetProps {
  htmlContent: string;
  portfolioName: string;
  symbols: string[];
  period: string;
  dataPoints: number;
  onNewAnalysis: () => void;
}

export default function QuantStatsTearsheet({
  htmlContent,
  portfolioName,
  symbols,
  period,
  dataPoints,
  onNewAnalysis,
}: QuantStatsTearsheetProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with portfolio info and controls */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                {portfolioName}
              </h1>
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <span>
                  <strong>Symbols:</strong> {symbols.join(', ')}
                </span>
                <span>
                  <strong>Period:</strong> {period}
                </span>
                <span>
                  <strong>Data Points:</strong> {dataPoints}
                </span>
              </div>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={onNewAnalysis}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                New Analysis
              </button>
            </div>
          </div>
        </div>

        {/* QuantStats HTML Tearsheet */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div 
            className="quantstats-tearsheet"
            dangerouslySetInnerHTML={{ __html: htmlContent }}
            style={{
              // Ensure the tearsheet is properly styled and responsive
              maxWidth: '100%',
              overflow: 'auto'
            }}
          />
        </div>

        {/* Footer with additional actions */}
        <div className="mt-8 text-center">
          <div className="bg-blue-50 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-2">
              Analysis Complete
            </h3>
            <p className="text-blue-700 mb-4">
              Your QuantStats tearsheet is ready. The analysis includes comprehensive
              portfolio metrics, performance visualizations, and risk assessment.
            </p>
            <div className="flex justify-center space-x-4">
              <button
                onClick={onNewAnalysis}
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
      </div>
    </div>
  );
}