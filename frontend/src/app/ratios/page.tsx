'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { PortfolioAPI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Loader2 } from 'lucide-react';

interface RatioRowData {
  [key: string]: string | number | null;
}

interface SymbolRatioData {
  data: RatioRowData[];
  columns: string[];
}

interface RatiosResponse {
  symbols?: string[];
  ratio_data: Record<string, SymbolRatioData>;
  summary_data: RatioRowData[];
}

export default function RatiosPage() {
  const [symbols, setSymbols] = useState('');
  const [period, setPeriod] = useState('year');
  const [submittedSymbols, setSubmittedSymbols] = useState<string>('');

  const { data: ratiosData, isLoading, error } = useQuery<RatiosResponse | null>({
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
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!submittedSymbols || !ratiosData ? (
          // Input Form
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold mb-4">
                Financial Ratios Analysis
              </h1>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Analyze financial ratios for Vietnamese stocks including P/E, P/B, ROE, ROA, and more.
              </p>
            </div>

            <div className="max-w-2xl mx-auto">
              <Card>
                <CardHeader>
                  <CardTitle>Stock Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="symbols">
                        Stock Symbols
                      </Label>
                      <Input
                        type="text"
                        id="symbols"
                        value={symbols}
                        onChange={(e) => setSymbols(e.target.value)}
                        placeholder="Enter stock symbols separated by commas (e.g., VNM, VIC, FPT)"
                        required
                      />
                      <p className="text-sm text-muted-foreground">
                        Enter Vietnamese stock symbols separated by commas
                      </p>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="period">
                        Period
                      </Label>
                      <Select
                        id="period"
                        value={period}
                        onChange={(e) => setPeriod(e.target.value)}
                      >
                        <option value="year">Annual</option>
                        <option value="quarter">Quarterly</option>
                      </Select>
                    </div>

                    <Button
                      type="submit"
                      disabled={isLoading || !symbols.trim()}
                      className="w-full"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        'Analyze Ratios'
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        ) : (
          // Results
          <div className="space-y-8">
            {/* Header */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-2xl">
                      Financial Ratios Analysis
                    </CardTitle>
                    <div className="mt-2 flex flex-wrap gap-2 text-sm text-muted-foreground">
                      <div className="flex flex-wrap gap-1">
                        <span className="font-medium">Symbols:</span>
                        {(ratiosData?.symbols || submittedSymbols.split(',').map(s => s.trim())).map((symbol: string) => (
                          <Badge key={symbol} variant="secondary">{symbol}</Badge>
                        ))}
                      </div>
                      <Badge variant="outline">
                        Period: {period === 'year' ? 'Annual' : 'Quarterly'}
                      </Badge>
                    </div>
                  </div>
                  <Button onClick={handleNewAnalysis}>
                    New Analysis
                  </Button>
                </div>
              </CardHeader>
            </Card>

            {/* Error Display */}
            {error && (
              <Card className="border-destructive bg-destructive/10">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium text-destructive">
                    Analysis Error
                  </h3>
                  <div className="mt-2 text-sm text-destructive">
                    {error instanceof Error ? error.message : 'An error occurred while fetching ratio data'}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Loading State */}
            {isLoading && (
              <Card className="p-8 text-center">
                <Loader2 className="h-8 w-8 animate-spin mx-auto" />
                <p className="mt-2 text-muted-foreground">Fetching financial ratios...</p>
              </Card>
            )}

            {/* Ratios Data */}
            {ratiosData && ratiosData.ratio_data && (
              <div className="space-y-6">
                {Object.entries(ratiosData.ratio_data).map(([symbol, data]) => (
                  <Card key={symbol}>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Badge variant="default">{symbol}</Badge>
                        <span>Financial Ratios</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {data.data && data.data.length > 0 ? (
                        <Table>
                          <TableHeader>
                            <TableRow>
                              {data.columns.map((column: string) => (
                                <TableHead key={column}>
                                  {column}
                                </TableHead>
                              ))}
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {data.data.map((row, idx) => (
                              <TableRow key={idx}>
                                {data.columns.map((column: string) => (
                                  <TableCell key={column}>
                                    {typeof row[column] === 'number' 
                                      ? row[column].toLocaleString()
                                      : row[column] || '-'
                                    }
                                  </TableCell>
                                ))}
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      ) : (
                        <div className="text-center py-8">
                          <p className="text-muted-foreground">No ratio data available for {symbol}</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Summary Data */}
            {ratiosData && ratiosData.summary_data && ratiosData.summary_data.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Fundamental Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        {Object.keys(ratiosData.summary_data[0]).map((key) => (
                          <TableHead key={key}>
                            {key}
                          </TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {ratiosData.summary_data.map((row, idx) => (
                        <TableRow key={idx}>
                          {Object.values(row).map((value, colIdx) => (
                            <TableCell key={colIdx}>
                              {typeof value === 'number' 
                                ? value.toLocaleString()
                                : value || '-'
                              }
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
}