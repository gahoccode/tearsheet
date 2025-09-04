import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone builds for Docker deployment
  output: 'standalone',
  
  // Optimize for production builds
  experimental: {
    // Enable experimental features if needed
    turbo: {
      // Turbopack configuration
    }
  },
  
  // Environment variable configuration
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};

export default nextConfig;
