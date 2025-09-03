'use client';

import { useRef, useEffect } from 'react';

interface PlotlyData {
  x?: any[];
  y?: any[];
  z?: any[];
  type: string;
  mode?: string;
  name?: string;
  marker?: any;
  line?: any;
  values?: number[];
  labels?: string[];
  [key: string]: any;
}

interface PlotlyLayout {
  title?: string | { text: string; [key: string]: any };
  xaxis?: any;
  yaxis?: any;
  width?: number;
  height?: number;
  showlegend?: boolean;
  margin?: any;
  [key: string]: any;
}

interface DynamicPlotlyChartProps {
  data: PlotlyData[];
  layout?: PlotlyLayout;
  config?: any;
  title?: string;
  className?: string;
}

declare global {
  interface Window {
    Plotly: any;
  }
}

export default function DynamicPlotlyChart({ 
  data, 
  layout = {}, 
  config = {}, 
  title,
  className = "" 
}: DynamicPlotlyChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const plotlyLoadedRef = useRef(false);

  const loadPlotly = (): Promise<any> => {
    return new Promise((resolve, reject) => {
      if (window.Plotly) {
        resolve(window.Plotly);
        return;
      }

      if (plotlyLoadedRef.current) {
        // Already loading, wait for it
        const checkPlotly = () => {
          if (window.Plotly) {
            resolve(window.Plotly);
          } else {
            setTimeout(checkPlotly, 100);
          }
        };
        checkPlotly();
        return;
      }

      plotlyLoadedRef.current = true;

      const script = document.createElement('script');
      script.src = 'https://cdn.plot.ly/plotly-2.35.2.min.js';
      script.async = true;
      script.onload = () => {
        resolve(window.Plotly);
      };
      script.onerror = (error) => {
        plotlyLoadedRef.current = false;
        reject(error);
      };
      document.head.appendChild(script);
    });
  };

  const createPlot = async () => {
    if (!containerRef.current || !data?.length) return;

    try {
      const Plotly = await loadPlotly();
      
      const plotLayout = {
        ...layout,
        responsive: true,
        autosize: true,
        ...((title && !layout.title) && { title: { text: title } })
      };

      const plotConfig = {
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        ...config
      };

      // Clear the container
      containerRef.current.innerHTML = '';

      // Create the plot
      await Plotly.newPlot(containerRef.current, data, plotLayout, plotConfig);
    } catch (error) {
      console.error('Error creating Plotly chart:', error);
      if (containerRef.current) {
        containerRef.current.innerHTML = `
          <div class="flex items-center justify-center h-64 bg-gray-100 rounded-lg">
            <p class="text-gray-500">Failed to load chart</p>
          </div>
        `;
      }
    }
  };

  useEffect(() => {
    createPlot();
  }, [data, layout, config, title]);

  useEffect(() => {
    const handleResize = () => {
      if (window.Plotly && containerRef.current) {
        window.Plotly.Plots.resize(containerRef.current);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
      {title && (
        <h2 className="text-xl font-semibold text-gray-900 mb-4">{title}</h2>
      )}
      <div 
        ref={containerRef} 
        className="w-full h-96 min-h-[400px]"
        style={{ minHeight: '400px' }}
      />
    </div>
  );
}