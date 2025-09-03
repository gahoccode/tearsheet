import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ReactQueryProvider } from "@/lib/react-query";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Vietnam Stock Portfolio Analyzer",
  description: "Analyze your Vietnamese stock portfolio with interactive visualizations and comprehensive performance metrics",
  keywords: ["portfolio", "vietnam stocks", "analysis", "vnstock", "investment"],
  authors: [{ name: "Portfolio Analyzer" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased bg-gray-50 min-h-screen`}>
        <ReactQueryProvider>
          <div className="min-h-screen">
            <header className="bg-white shadow-sm border-b border-gray-200">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                  <div className="flex items-center">
                    <h1 className="text-xl font-bold text-gray-900">
                      Vietnam Stock Portfolio Analyzer
                    </h1>
                  </div>
                  <nav className="flex space-x-4">
                    <a
                      href="/"
                      className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      Portfolio Analysis
                    </a>
                    <a
                      href="/ratios"
                      className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      Financial Ratios
                    </a>
                  </nav>
                </div>
              </div>
            </header>
            <main className="flex-1">
              {children}
            </main>
            <footer className="bg-white border-t border-gray-200 mt-auto">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <p className="text-center text-sm text-gray-500">
                  Powered by vnstock API • Built with Next.js & Flask
                </p>
              </div>
            </footer>
          </div>
        </ReactQueryProvider>
      </body>
    </html>
  );
}
