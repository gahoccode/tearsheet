'use client';

import { useEffect, useRef } from 'react';

interface PlotlyChartProps {
  htmlContent: string;
  title?: string;
  className?: string;
}

export default function PlotlyChart({ htmlContent, title, className = "" }: PlotlyChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current && htmlContent) {
      // Clear previous content
      containerRef.current.innerHTML = '';
      
      try {
        // Create a temporary div to parse the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = htmlContent;
        
        // Find the chart div
        const chartDiv = tempDiv.querySelector('div[class="plotly-graph-div"]');
        const scriptTag = tempDiv.querySelector('script');
        
        if (chartDiv && scriptTag) {
          // Append the chart div to our container
          containerRef.current.appendChild(chartDiv.cloneNode(true));
          
          // Execute the script to render the Plotly chart
          const script = document.createElement('script');
          script.text = scriptTag.textContent || '';
          document.body.appendChild(script);
          
          // Clean up script after execution
          setTimeout(() => {
            document.body.removeChild(script);
          }, 100);
        } else {
          // Fallback: insert all HTML content
          containerRef.current.innerHTML = htmlContent;
        }
      } catch (error) {
        console.error('Error rendering Plotly chart:', error);
        // Fallback: insert raw HTML
        containerRef.current.innerHTML = htmlContent;
      }
    }
  }, [htmlContent]);

  if (!htmlContent) {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-lg ${className}`}>
        <div className="flex items-center justify-center h-64 text-gray-500">
          <div className="text-center">
            <div className="text-lg font-medium">Chart Loading...</div>
            <div className="text-sm">Generating visualization</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {title && (
        <div className="px-6 pt-6 pb-2">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
      )}
      <div ref={containerRef} className="plotly-chart-container p-4" />
    </div>
  );
}