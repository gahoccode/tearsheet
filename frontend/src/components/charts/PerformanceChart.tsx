'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ReturnsData } from '@/types/portfolio';
import { formatPercentage, formatDate } from '@/lib/api';

interface PerformanceChartProps {
  returns: ReturnsData;
  title?: string;
}

export default function PerformanceChart({ returns, title = "Portfolio Performance" }: PerformanceChartProps) {
  // Transform data for Recharts
  const chartData = returns.dates.map((date, index) => {
    // Calculate cumulative return
    const cumulativeReturn = returns.values.slice(0, index + 1).reduce((acc, val) => {
      return acc * (1 + val);
    }, 1) - 1;

    return {
      date,
      dateFormatted: formatDate(date),
      return: cumulativeReturn * 100, // Convert to percentage
      dailyReturn: returns.values[index] * 100,
    };
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{data.dateFormatted}</p>
          <p className="text-blue-600">
            Cumulative Return: {formatPercentage(data.return / 100, 2)}
          </p>
          <p className="text-gray-600">
            Daily Return: {formatPercentage(data.dailyReturn / 100, 2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="dateFormatted" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `${value.toFixed(1)}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="return" 
              stroke="#2563eb" 
              strokeWidth={2}
              dot={false}
              name="Cumulative Return (%)"
              activeDot={{ r: 4, fill: '#2563eb' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}