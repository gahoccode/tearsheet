import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { ReactQueryProvider } from "@/lib/react-query";
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/ui/theme-toggle";

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
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <ReactQueryProvider>
          <div className="min-h-screen">
            <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                  <div className="flex items-center">
                    <h1 className="text-xl font-bold text-foreground">
                      Vietnam Stock Portfolio Analyzer
                    </h1>
                  </div>
                  <nav className="flex items-center space-x-4">
                    <Link
                      href="/"
                      className="text-muted-foreground hover:text-foreground px-3 py-2 rounded-md text-sm font-medium transition-colors"
                    >
                      Portfolio Analysis
                    </Link>
                    <Link
                      href="/ratios"
                      className="text-muted-foreground hover:text-foreground px-3 py-2 rounded-md text-sm font-medium transition-colors"
                    >
                      Financial Ratios
                    </Link>
                    <ThemeToggle />
                  </nav>
                </div>
              </div>
            </header>
            <main className="flex-1">
              {children}
            </main>
            <footer className="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 mt-auto">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <p className="text-center text-sm text-muted-foreground">
                  Powered by vnstock API • Built with Next.js & Flask
                </p>
              </div>
            </footer>
          </div>
          </ReactQueryProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
