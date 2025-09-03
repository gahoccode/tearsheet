'use client';

import { PerformanceMetrics } from '@/types/portfolio';
import { formatPercentage, formatDate } from '@/lib/api';

interface MetricsDashboardProps {
  metrics: PerformanceMetrics;
}

interface MetricCardProps {
  title: string;
  value: string;
  description?: string;
  colorClass?: string;
  icon?: React.ReactNode;
}

function MetricCard({ title, value, description, colorClass = "text-blue-600", icon }: MetricCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border-l-4 border-blue-500">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</h3>
          <p className={`text-2xl font-bold ${colorClass} mt-1`}>{value}</p>
          {description && (
            <p className="text-sm text-gray-600 mt-1">{description}</p>
          )}
        </div>
        {icon && (
          <div className="ml-4 text-gray-400">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

const TrendUpIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
  </svg>
);

const TrendDownIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
  </svg>
);

const AnalyticsIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>
);

const RiskIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L4.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
  </svg>
);

const CalendarIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const getReturnColorClass = (value: number) => {
  if (value > 0) return "text-green-600";
  if (value < 0) return "text-red-600";
  return "text-gray-600";
};

const getReturnIcon = (value: number) => {
  if (value > 0) return <TrendUpIcon />;
  if (value < 0) return <TrendDownIcon />;
  return <AnalyticsIcon />;
};

const getRiskLevel = (sharpeRatio: number, volatility: number) => {
  if (sharpeRatio > 1 && volatility < 0.15) return { level: "Low", color: "text-green-600" };
  if (sharpeRatio > 0.5 && volatility < 0.25) return { level: "Medium", color: "text-yellow-600" };
  return { level: "High", color: "text-red-600" };
};

export default function MetricsDashboard({ metrics }: MetricsDashboardProps) {
  const riskAssessment = getRiskLevel(metrics.sharpe_ratio, metrics.volatility);
  
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Performance Metrics</h2>
        <p className="text-gray-600 mb-6">
          Analysis period: {formatDate(metrics.start_date)} to {formatDate(metrics.end_date)} 
          ({metrics.total_periods} trading days)
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MetricCard
          title="Total Return"
          value={formatPercentage(metrics.total_return, 2)}
          description="Cumulative portfolio return"
          colorClass={getReturnColorClass(metrics.total_return)}
          icon={getReturnIcon(metrics.total_return)}
        />

        <MetricCard
          title="Annualized Return"
          value={formatPercentage(metrics.annualized_return, 2)}
          description="Expected annual return"
          colorClass={getReturnColorClass(metrics.annualized_return)}
          icon={<CalendarIcon />}
        />

        <MetricCard
          title="Volatility"
          value={formatPercentage(metrics.volatility, 2)}
          description="Annualized standard deviation"
          colorClass="text-orange-600"
          icon={<AnalyticsIcon />}
        />

        <MetricCard
          title="Sharpe Ratio"
          value={metrics.sharpe_ratio.toFixed(3)}
          description="Risk-adjusted return measure"
          colorClass={metrics.sharpe_ratio > 1 ? "text-green-600" : metrics.sharpe_ratio > 0 ? "text-yellow-600" : "text-red-600"}
          icon={<AnalyticsIcon />}
        />

        <MetricCard
          title="Maximum Drawdown"
          value={formatPercentage(Math.abs(metrics.max_drawdown), 2)}
          description="Largest peak-to-trough decline"
          colorClass="text-red-600"
          icon={<TrendDownIcon />}
        />

        <MetricCard
          title="Win Rate"
          value={formatPercentage(metrics.win_rate, 1)}
          description="Percentage of positive trading days"
          colorClass={metrics.win_rate > 0.5 ? "text-green-600" : "text-red-600"}
          icon={<AnalyticsIcon />}
        />
      </div>

      {/* Risk Assessment */}
      <div className="bg-white p-6 rounded-lg shadow-lg border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Assessment</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className={`text-2xl font-bold ${riskAssessment.color} mb-1`}>
              {riskAssessment.level}
            </div>
            <div className="text-sm text-gray-600">Risk Level</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-1">
              {(metrics.sharpe_ratio > 0 ? "Good" : "Poor")}
            </div>
            <div className="text-sm text-gray-600">Risk-Adjusted Performance</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${metrics.max_drawdown < -0.1 ? "text-red-600" : "text-green-600"} mb-1`}>
              {Math.abs(metrics.max_drawdown) < 0.1 ? "Stable" : "Volatile"}
            </div>
            <div className="text-sm text-gray-600">Drawdown Profile</div>
          </div>
        </div>

        {/* Risk Interpretation */}
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">Interpretation</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>
              <strong>Sharpe Ratio:</strong> {
                metrics.sharpe_ratio > 1 ? "Excellent risk-adjusted returns" :
                metrics.sharpe_ratio > 0.5 ? "Good risk-adjusted returns" :
                metrics.sharpe_ratio > 0 ? "Moderate risk-adjusted returns" :
                "Poor risk-adjusted returns"
              }
            </li>
            <li>
              <strong>Volatility:</strong> {
                metrics.volatility < 0.15 ? "Low volatility portfolio" :
                metrics.volatility < 0.25 ? "Moderate volatility" :
                "High volatility portfolio"
              }
            </li>
            <li>
              <strong>Max Drawdown:</strong> {
                Math.abs(metrics.max_drawdown) < 0.1 ? "Conservative drawdown levels" :
                Math.abs(metrics.max_drawdown) < 0.2 ? "Moderate drawdown levels" :
                "High drawdown levels - consider risk management"
              }
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}