'use client';

import { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { PortfolioAPI } from '@/lib/api';
import { PortfolioFormData } from '@/types/portfolio';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

// Validation schema using Zod
const portfolioSchema = z.object({
  name: z.string().optional(),
  capital: z.number().min(1000000, 'Capital must be at least 1,000,000 VND'),
  start_date: z.string().refine((date) => !isNaN(Date.parse(date)), 'Invalid start date'),
  end_date: z.string().refine((date) => !isNaN(Date.parse(date)), 'Invalid end date'),
  stocks: z.array(z.object({
    symbol: z.string().min(3, 'Symbol must be at least 3 characters').max(4, 'Symbol must be at most 4 characters'),
    weight: z.number().min(0.01, 'Weight must be at least 1%').max(1, 'Weight cannot exceed 100%'),
  })).min(1, 'At least one stock is required').max(10, 'Maximum 10 stocks allowed'),
}).refine((data) => {
  const totalWeight = data.stocks.reduce((sum, stock) => sum + stock.weight, 0);
  return Math.abs(totalWeight - 1) < 0.01;
}, {
  message: 'Total weights must sum to 100%',
  path: ['stocks'],
});

type PortfolioFormValues = z.infer<typeof portfolioSchema>;

interface TearsheetResponse {
  html: string;
  portfolio_name: string;
  symbols: string[];
  period: string;
  data_points: number;
}

interface PortfolioFormProps {
  onAnalysisComplete: (data: TearsheetResponse) => void;
}

export default function PortfolioForm({ onAnalysisComplete }: PortfolioFormProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const {
    register,
    control,
    handleSubmit,
    watch,
    formState: { errors },
    setError,
    clearErrors,
  } = useForm<PortfolioFormValues>({
    resolver: zodResolver(portfolioSchema),
    defaultValues: {
      name: '',
      capital: 10000000,
      start_date: '2024-01-01',
      end_date: '2024-06-30',
      stocks: [
        { symbol: 'REE', weight: 0.4 },
        { symbol: 'FMC', weight: 0.35 },
        { symbol: 'DHC', weight: 0.25 },
      ],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'stocks',
  });

  const stocks = watch('stocks');
  const totalWeight = stocks?.reduce((sum, stock) => sum + (stock.weight || 0), 0) || 0;

  const analyzeMutation = useMutation({
    mutationFn: async (data: PortfolioFormValues) => {
      const formData: PortfolioFormData = {
        symbols: data.stocks.map(s => s.symbol),
        weights: data.stocks.map(s => s.weight),
        capital: data.capital,
        start_date: data.start_date,
        end_date: data.end_date,
        name: data.name,
      };
      return PortfolioAPI.generateTearsheet(formData);
    },
    onSuccess: (data) => {
      onAnalysisComplete(data);
      setIsAnalyzing(false);
    },
    onError: (error: Error) => {
      setError('root', { message: error.message });
      setIsAnalyzing(false);
    },
  });

  const onSubmit = async (data: PortfolioFormValues) => {
    clearErrors();
    setIsAnalyzing(true);
    analyzeMutation.mutate(data);
  };

  const addStock = () => {
    if (fields.length < 10) {
      append({ symbol: '', weight: 0 });
    }
  };

  const removeStock = (index: number) => {
    if (fields.length > 1) {
      remove(index);
    }
  };

  return (
    <Card className="max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl">Portfolio Analysis</CardTitle>
        <CardDescription>
          Analyze your Vietnamese stock portfolio with interactive visualizations
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Portfolio Name */}
        <div className="space-y-2">
          <Label htmlFor="name">
            Portfolio Name (Optional)
          </Label>
          <Input
            {...register('name')}
            type="text"
            placeholder="My Portfolio"
          />
        </div>

        {/* Capital */}
        <div className="space-y-2">
          <Label htmlFor="capital">
            Initial Capital (VND)
          </Label>
          <Input
            {...register('capital', { valueAsNumber: true })}
            type="number"
            step="1000000"
            min="1000000"
          />
          {errors.capital && (
            <p className="mt-1 text-sm text-destructive">{errors.capital.message}</p>
          )}
        </div>

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="start_date">
              Start Date
            </Label>
            <Input
              {...register('start_date')}
              type="date"
            />
            {errors.start_date && (
              <p className="mt-1 text-sm text-destructive">{errors.start_date.message}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="end_date">
              End Date
            </Label>
            <Input
              {...register('end_date')}
              type="date"
            />
            {errors.end_date && (
              <p className="mt-1 text-sm text-destructive">{errors.end_date.message}</p>
            )}
          </div>
        </div>

        {/* Stocks */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium">Portfolio Composition</h3>
            <Button
              type="button"
              onClick={addStock}
              disabled={fields.length >= 10}
              variant="outline"
            >
              Add Stock
            </Button>
          </div>

          <div className="space-y-4">
            {fields.map((field, index) => (
              <Card key={field.id} className="p-4">
                <div className="flex items-center space-x-4">
                  <div className="flex-1 space-y-2">
                    <Label htmlFor={`stocks.${index}.symbol`}>
                      Symbol
                    </Label>
                    <Input
                      {...register(`stocks.${index}.symbol`)}
                      type="text"
                      placeholder="REE"
                    />
                    {errors.stocks?.[index]?.symbol && (
                      <p className="mt-1 text-sm text-destructive">
                        {errors.stocks[index]?.symbol?.message}
                      </p>
                    )}
                  </div>

                  <div className="flex-1 space-y-2">
                    <Label htmlFor={`stocks.${index}.weight`}>
                      Weight (%)
                    </Label>
                    <Input
                      {...register(`stocks.${index}.weight`, { valueAsNumber: true })}
                      type="number"
                      step="0.01"
                      min="0.01"
                      max="1"
                      placeholder="0.40"
                    />
                    {errors.stocks?.[index]?.weight && (
                      <p className="mt-1 text-sm text-destructive">
                        {errors.stocks[index]?.weight?.message}
                      </p>
                    )}
                  </div>

                  <Button
                    type="button"
                    onClick={() => removeStock(index)}
                    disabled={fields.length <= 1}
                    variant="destructive"
                    size="sm"
                    className="mt-6"
                  >
                    Remove
                  </Button>
                </div>
              </Card>
            ))}
          </div>

          {/* Weight Summary */}
          <Card className="mt-4 p-3 bg-muted">
            <p className="text-sm">
              Total Weight: {(totalWeight * 100).toFixed(2)}%
              {Math.abs(totalWeight - 1) > 0.01 && (
                <span className="ml-2 text-destructive">
                  (Must equal 100%)
                </span>
              )}
            </p>
          </Card>

          {errors.stocks && typeof errors.stocks.message === 'string' && (
            <p className="mt-1 text-sm text-destructive">{errors.stocks.message}</p>
          )}
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <Button
            type="submit"
            disabled={isAnalyzing || Math.abs(totalWeight - 1) > 0.01}
            className="w-full"
            size="lg"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing Portfolio...
              </>
            ) : (
              'Analyze Portfolio'
            )}
          </Button>
        </div>

        {/* Error Messages */}
        {errors.root && (
          <Card className="p-4 border-destructive bg-destructive/10">
            <p className="text-sm text-destructive">{errors.root.message}</p>
          </Card>
        )}
      </form>
      </CardContent>
    </Card>
  );
}