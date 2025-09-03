'use client';

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { ReturnsData } from '@/types/portfolio';
import { formatPercentage, formatDate } from '@/lib/api';

interface DrawdownChartProps {
  returns: ReturnsData;
  title?: string;
}

export default function DrawdownChart({ returns, title = "Portfolio Drawdown" }: DrawdownChartProps) {
  // Calculate drawdown data
  const chartData = returns.dates.map((date, index) => {
    // Calculate cumulative return up to this point
    const cumulativeReturn = returns.values.slice(0, index + 1).reduce((acc, val) => {
      return acc * (1 + val);
    }, 1);
    
    // Calculate running maximum
    const runningMax = returns.values.slice(0, index + 1).reduce((maxAcc, val, i) => {
      const currentCumulative = returns.values.slice(0, i + 1).reduce((acc, v) => acc * (1 + v), 1);
      return Math.max(maxAcc, currentCumulative);
    }, 1);
    
    // Calculate drawdown
    const drawdown = ((cumulativeReturn / runningMax) - 1) * 100;

    return {
      date,
      dateFormatted: formatDate(date),
      drawdown,
      cumulativeReturn: (cumulativeReturn - 1) * 100,
    };
  });

  const maxDrawdown = Math.min(...chartData.map(d => d.drawdown));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{data.dateFormatted}</p>
          <p className="text-red-600">
            Drawdown: {formatPercentage(data.drawdown / 100, 2)}
          </p>
          <p className="text-blue-600">
            Portfolio Return: {formatPercentage(data.cumulativeReturn / 100, 2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="text-sm text-gray-600">
          Max Drawdown: <span className="font-semibold text-red-600">
            {formatPercentage(maxDrawdown / 100, 2)}
          </span>
        </div>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <defs>
              <linearGradient id="drawdownGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#dc2626" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#dc2626" stopOpacity={0.2}/>
              </linearGradient>
            </defs>
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
            <ReferenceLine y={0} stroke="#666" strokeDasharray="2 2" />
            <Area
              type="monotone"
              dataKey="drawdown"
              stroke="#dc2626"
              fillOpacity={1}
              fill="url(#drawdownGradient)"
              name="Drawdown (%)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}