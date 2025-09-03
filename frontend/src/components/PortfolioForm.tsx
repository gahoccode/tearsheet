'use client';

import { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { PortfolioAPI } from '@/lib/api';
import { PortfolioFormData, PortfolioAnalysisResponse } from '@/types/portfolio';

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

interface PortfolioFormProps {
  onAnalysisComplete: (data: PortfolioAnalysisResponse) => void;
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
      return PortfolioAPI.analyzePortfolio(formData);
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
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Portfolio Analysis</h2>
        <p className="text-gray-600">
          Analyze your Vietnamese stock portfolio with interactive visualizations
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Portfolio Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Portfolio Name (Optional)
          </label>
          <input
            {...register('name')}
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="My Portfolio"
          />
        </div>

        {/* Capital */}
        <div>
          <label htmlFor="capital" className="block text-sm font-medium text-gray-700 mb-1">
            Initial Capital (VND)
          </label>
          <input
            {...register('capital', { valueAsNumber: true })}
            type="number"
            step="1000000"
            min="1000000"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          {errors.capital && (
            <p className="mt-1 text-sm text-red-600">{errors.capital.message}</p>
          )}
        </div>

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-1">
              Start Date
            </label>
            <input
              {...register('start_date')}
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {errors.start_date && (
              <p className="mt-1 text-sm text-red-600">{errors.start_date.message}</p>
            )}
          </div>
          <div>
            <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-1">
              End Date
            </label>
            <input
              {...register('end_date')}
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {errors.end_date && (
              <p className="mt-1 text-sm text-red-600">{errors.end_date.message}</p>
            )}
          </div>
        </div>

        {/* Stocks */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Portfolio Composition</h3>
            <button
              type="button"
              onClick={addStock}
              disabled={fields.length >= 10}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Add Stock
            </button>
          </div>

          <div className="space-y-4">
            {fields.map((field, index) => (
              <div key={field.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-md">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Symbol
                  </label>
                  <input
                    {...register(`stocks.${index}.symbol`)}
                    type="text"
                    placeholder="REE"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  {errors.stocks?.[index]?.symbol && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.stocks[index]?.symbol?.message}
                    </p>
                  )}
                </div>

                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Weight (%)
                  </label>
                  <input
                    {...register(`stocks.${index}.weight`, { valueAsNumber: true })}
                    type="number"
                    step="0.01"
                    min="0.01"
                    max="1"
                    placeholder="0.40"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  {errors.stocks?.[index]?.weight && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.stocks[index]?.weight?.message}
                    </p>
                  )}
                </div>

                <button
                  type="button"
                  onClick={() => removeStock(index)}
                  disabled={fields.length <= 1}
                  className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed mt-6"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          {/* Weight Summary */}
          <div className="mt-4 p-3 bg-blue-50 rounded-md">
            <p className="text-sm text-blue-800">
              Total Weight: {(totalWeight * 100).toFixed(2)}%
              {Math.abs(totalWeight - 1) > 0.01 && (
                <span className="ml-2 text-red-600">
                  (Must equal 100%)
                </span>
              )}
            </p>
          </div>

          {errors.stocks && typeof errors.stocks.message === 'string' && (
            <p className="mt-1 text-sm text-red-600">{errors.stocks.message}</p>
          )}
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isAnalyzing || Math.abs(totalWeight - 1) > 0.01}
            className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Analyzing Portfolio...
              </div>
            ) : (
              'Analyze Portfolio'
            )}
          </button>
        </div>

        {/* Error Messages */}
        {errors.root && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{errors.root.message}</p>
          </div>
        )}
      </form>
    </div>
  );
}