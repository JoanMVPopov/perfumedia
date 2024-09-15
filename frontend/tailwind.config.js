/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/**/*.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#C96868',    // Color 1
        secondary: '#FADFA1',  // Color 2
        light: '#FFF4EA',      // Color 3
        accent: '#7EACB5',     // Color 4
      },
    },
  },
  plugins: [],
}

