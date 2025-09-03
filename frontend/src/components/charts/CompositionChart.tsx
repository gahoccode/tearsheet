'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Stock } from '@/types/portfolio';
import { formatCurrency, formatPercentage } from '@/lib/api';

interface CompositionChartProps {
  stocks: Stock[];
  capital: number;
  title?: string;
}

// Color palette for the pie chart
const COLORS = [
  '#2563eb', '#dc2626', '#16a34a', '#ca8a04', '#9333ea',
  '#c2410c', '#0891b2', '#be185d', '#4338ca', '#059669'
];

export default function CompositionChart({ stocks, capital, title = "Portfolio Composition" }: CompositionChartProps) {
  // Transform data for the pie chart
  const chartData = stocks.map((stock, index) => ({
    name: stock.symbol,
    weight: stock.weight * 100, // Convert to percentage
    value: stock.weight * capital, // Actual allocation amount
    color: COLORS[index % COLORS.length],
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{data.name}</p>
          <p className="text-blue-600">
            Weight: {formatPercentage(data.weight / 100, 1)}
          </p>
          <p className="text-green-600">
            Allocation: {formatCurrency(data.value)}
          </p>
        </div>
      );
    }
    return null;
  };

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    if (percent < 0.05) return null; // Don't show labels for very small slices
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={100}
              fill="#8884d8"
              dataKey="weight"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              formatter={(value, entry: any) => (
                <span style={{ color: entry.color, fontWeight: 'bold' }}>
                  {value} ({formatPercentage((entry.payload.weight / 100), 1)})
                </span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      {/* Summary Table */}
      <div className="mt-6">
        <h4 className="text-md font-medium text-gray-900 mb-3">Allocation Breakdown</h4>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Symbol</th>
                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Weight</th>
                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 uppercase">Allocation</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stocks.map((stock, index) => (
                <tr key={stock.symbol} className="hover:bg-gray-50">
                  <td className="px-3 py-2 whitespace-nowrap">
                    <div className="flex items-center">
                      <div 
                        className="w-3 h-3 rounded-full mr-2"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      ></div>
                      <span className="font-medium text-gray-900">{stock.symbol}</span>
                    </div>
                  </td>
                  <td className="px-3 py-2 whitespace-nowrap text-right text-sm text-gray-900">
                    {formatPercentage(stock.weight, 1)}
                  </td>
                  <td className="px-3 py-2 whitespace-nowrap text-right text-sm text-gray-900">
                    {formatCurrency(stock.weight * capital)}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-gray-50">
              <tr>
                <td className="px-3 py-2 whitespace-nowrap font-medium text-gray-900">Total</td>
                <td className="px-3 py-2 whitespace-nowrap text-right font-medium text-gray-900">100.0%</td>
                <td className="px-3 py-2 whitespace-nowrap text-right font-medium text-gray-900">
                  {formatCurrency(capital)}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  );
}