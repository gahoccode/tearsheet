'use client';

import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

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
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with portfolio info and controls */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-2xl mb-2">
                  {portfolioName}
                </CardTitle>
                <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
                  <div className="flex flex-wrap gap-1">
                    <span className="font-medium">Symbols:</span>
                    {symbols.map(symbol => (
                      <Badge key={symbol} variant="secondary">{symbol}</Badge>
                    ))}
                  </div>
                  <Badge variant="outline">
                    Period: {period}
                  </Badge>
                  <Badge variant="outline">
                    Data Points: {dataPoints}
                  </Badge>
                </div>
              </div>
              <div className="flex space-x-4">
                <Button onClick={onNewAnalysis}>
                  New Analysis
                </Button>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* QuantStats HTML Tearsheet */}
        <Card className="overflow-hidden">
          <CardContent className="p-0">
            <div 
              className="quantstats-tearsheet"
              dangerouslySetInnerHTML={{ __html: htmlContent }}
              style={{
                maxWidth: '100%',
                overflow: 'auto'
              }}
            />
          </CardContent>
        </Card>

        {/* Footer with additional actions */}
        <div className="mt-8 text-center">
          <Card className="p-6 bg-muted/50">
            <CardHeader>
              <CardTitle className="text-lg mb-2">
                Analysis Complete
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                Your QuantStats tearsheet is ready. The analysis includes comprehensive
                portfolio metrics, performance visualizations, and risk assessment.
              </p>
              <div className="flex justify-center space-x-4">
                <Button
                  onClick={onNewAnalysis}
                  variant="outline"
                >
                  Analyze Different Portfolio
                </Button>
                <Button asChild>
                  <a href="/ratios">
                    View Financial Ratios
                  </a>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}