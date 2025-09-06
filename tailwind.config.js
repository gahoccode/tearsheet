/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      // Custom spacing to match QuantStats tearsheet measurements
      spacing: {
        18: "4.5rem", // 72px - custom gap
        30: "7.5rem", // 120px - large sections
      },
      // Custom max-widths for containers
      maxWidth: {
        form: "700px", // Form container max-width
        tearsheet: "960px", // Tearsheet container max-width
      },
      // Custom margins for chart alignment
      margin: {
        "-6": "-1.5rem", // -24px for SVG chart margins
      },
      // Typography to match QuantStats (Arial equivalent)
      fontFamily: {
        sans: [
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
      // Custom line heights for metrics alignment
      lineHeight: {
        5: "1.4", // Match QuantStats 1.4 line height
      },
      // Colors matching existing design
      colors: {
        primary: {
          50: "#f0f4ff",
          100: "#e0e7ff",
          600: "#1a237e", // Main brand color
          700: "#283593", // Hover state
        },
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("flowbite/plugin")],
};
