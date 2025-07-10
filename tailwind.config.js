/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {},
      colors: {
        ccblue: '#0D173F',
        ccred: '#FF0000',
      },
    },
  },
  plugins: [],
}
