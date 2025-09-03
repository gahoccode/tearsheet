'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { PortfolioAPI } from '@/lib/api';

interface RatioData {
  symbol: string;
  period: string;
  data: Record<string, any>[];
  columns: string[];
  rows: number;
}

export default function RatiosPage() {
  const [symbols, setSymbols] = useState('');
  const [period, setPeriod] = useState('year');
  const [submittedSymbols, setSubmittedSymbols] = useState<string>('');

  const { data: ratiosData, isLoading, error, refetch } = useQuery({
    queryKey: ['ratios', submittedSymbols, period],
    queryFn: async () => {
      if (!submittedSymbols) return null;
      const response = await PortfolioAPI.analyzeRatios({
        symbols: submittedSymbols,
        period: period
      });
      return response;
    },
    enabled: !!submittedSymbols
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symbols.trim()) {
      setSubmittedSymbols(symbols.trim());
    }
  };

  const handleNewAnalysis = () => {
    setSubmittedSymbols('');
    setSymbols('');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!submittedSymbols || !ratiosData ? (
          // Input Form
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Financial Ratios Analysis
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Analyze financial ratios for Vietnamese stocks including P/E, P/B, ROE, ROA, and more.
              </p>
            </div>

            <div className="max-w-2xl mx-auto">
              <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-lg space-y-6">
                <div>
                  <label htmlFor="symbols" className="block text-sm font-medium text-gray-700 mb-2">
                    Stock Symbols
                  </label>
                  <input
                    type="text"
                    id="symbols"
                    value={symbols}
                    onChange={(e) => setSymbols(e.target.value)}
                    placeholder="Enter stock symbols separated by commas (e.g., VNM, VIC, FPT)"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Enter Vietnamese stock symbols separated by commas
                  </p>
                </div>

                <div>
                  <label htmlFor="period" className="block text-sm font-medium text-gray-700 mb-2">
                    Period
                  </label>
                  <select
                    id="period"
                    value={period}
                    onChange={(e) => setPeriod(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="year">Annual</option>
                    <option value="quarter">Quarterly</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={isLoading || !symbols.trim()}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Analyzing...' : 'Analyze Ratios'}
                </button>
              </form>
            </div>
          </div>
        ) : (
          // Results
          <div className="space-y-8">
            {/* Header */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Financial Ratios Analysis
                  </h1>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
                    <span>
                      <strong>Symbols:</strong> {ratiosData?.symbols?.join(', ') || submittedSymbols}
                    </span>
                    <span>
                      <strong>Period:</strong> {period === 'year' ? 'Annual' : 'Quarterly'}
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

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      Analysis Error
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      {error instanceof Error ? error.message : 'An error occurred while fetching ratio data'}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p className="mt-2 text-gray-600">Fetching financial ratios...</p>
              </div>
            )}

            {/* Ratios Data */}
            {ratiosData && ratiosData.ratio_data && (
              <div className="space-y-6">
                {Object.entries(ratiosData.ratio_data).map(([symbol, data]: [string, any]) => (
                  <div key={symbol} className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      {symbol} - Financial Ratios
                    </h2>
                    
                    {data.data && data.data.length > 0 ? (
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              {data.columns.map((column: string) => (
                                <th
                                  key={column}
                                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                  {column}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {data.data.map((row: any, idx: number) => (
                              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                {data.columns.map((column: string) => (
                                  <td
                                    key={column}
                                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                  >
                                    {typeof row[column] === 'number' 
                                      ? row[column].toLocaleString()
                                      : row[column] || '-'
                                    }
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <div className="text-center py-8">
                        <p className="text-gray-500">No ratio data available for {symbol}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Summary Data */}
            {ratiosData && ratiosData.summary_data && ratiosData.summary_data.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Fundamental Summary
                </h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        {Object.keys(ratiosData.summary_data[0]).map((key) => (
                          <th
                            key={key}
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                          >
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {ratiosData.summary_data.map((row: any, idx: number) => (
                        <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          {Object.values(row).map((value: any, colIdx: number) => (
                            <td
                              key={colIdx}
                              className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                            >
                              {typeof value === 'number' 
                                ? value.toLocaleString()
                                : value || '-'
                              }
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}