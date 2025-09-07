import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import PortfolioForm from './components/PortfolioForm'
import ResultsPage from './components/ResultsPage'
import RatioPage from './components/RatioPage'
import 'antd/dist/reset.css'
import './App.css'

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1a237e',
        },
      }}
    >
      <Router>
        <div className="app">
          <Routes>
            <Route path="/" element={<PortfolioForm />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/ratio" element={<RatioPage />} />
          </Routes>
        </div>
      </Router>
    </ConfigProvider>
  )
}

export default App
