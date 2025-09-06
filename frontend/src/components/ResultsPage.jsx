import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Card, 
  Row, 
  Col, 
  Button, 
  Typography, 
  Space, 
  Statistic,
  Spin,
  Alert,
  Image
} from 'antd'
import { 
  BarChartOutlined, 
  HomeOutlined, 
  FileTextOutlined,
  ArrowLeftOutlined 
} from '@ant-design/icons'
import axios from 'axios'

const { Title } = Typography

function ResultsPage() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    try {
      const response = await axios.get('/results', {
        headers: {
          'Accept': 'application/json'
        }
      })
      if (response.data.error) {
        setError(response.data.error)
        setTimeout(() => navigate('/'), 3000)
      } else {
        setResults(response.data)
      }
    } catch (error) {
      console.error('Failed to fetch results:', error)
      setError('Failed to load results. Redirecting to home...')
      setTimeout(() => navigate('/'), 3000)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center' 
      }}>
        <Spin size="large" />
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        backgroundColor: '#f8f9fa', 
        padding: '40px 24px' 
      }}>
        <div style={{ maxWidth: 700, margin: '0 auto' }}>
          <Alert
            message="Error"
            description={error}
            type="error"
            showIcon
          />
        </div>
      </div>
    )
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f8f9fa', 
      padding: '40px 24px' 
    }}>
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <Card>
          <div style={{ marginBottom: 24 }}>
            <Title level={1}>
              <BarChartOutlined style={{ marginRight: 12 }} />
              Portfolio Analysis Results
            </Title>
            
            <Space>
              <Button 
                icon={<ArrowLeftOutlined />} 
                onClick={() => navigate('/')}
              >
                New Analysis
              </Button>
              <Button 
                type="primary" 
                icon={<FileTextOutlined />}
                onClick={() => window.open('/static/reports/quantstats-results.html', '_blank')}
              >
                View Full Report
              </Button>
            </Space>
          </div>

          {results && (
            <>
              {/* Portfolio Composition */}
              <Card title="Portfolio Composition" style={{ marginBottom: 24 }}>
                <Row gutter={16}>
                  {results.portfolio_symbols?.map((symbol, index) => (
                    <Col xs={24} sm={12} md={8} key={symbol}>
                      <Card size="small" style={{ textAlign: 'center' }}>
                        <Statistic
                          title={symbol}
                          value={parseFloat(results.portfolio_weights[index]) * 100}
                          precision={1}
                          suffix="%"
                        />
                      </Card>
                    </Col>
                  ))}
                </Row>
                
                <Row gutter={16} style={{ marginTop: 16 }}>
                  <Col xs={24} md={12}>
                    <Card size="small" style={{ textAlign: 'center' }}>
                      <Statistic
                        title="Analysis Period"
                        value={`${results.start_date} to ${results.end_date}`}
                        valueStyle={{ fontSize: '16px' }}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} md={12}>
                    <Card size="small" style={{ textAlign: 'center' }}>
                      <Statistic
                        title="Initial Capital"
                        value={results.capital}
                        formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                        suffix="VND"
                      />
                    </Card>
                  </Col>
                </Row>
              </Card>

              {/* Charts */}
              <Row gutter={[16, 16]}>
                {results.summary_chart_url && (
                  <Col xs={24}>
                    <Card title="Portfolio Summary" size="small">
                      <Image
                        src={results.summary_chart_url}
                        alt="Portfolio Summary"
                        style={{ width: '100%' }}
                      />
                    </Card>
                  </Col>
                )}
                
                {results.monthly_chart_url && (
                  <Col xs={24}>
                    <Card title="Monthly Returns Heatmap" size="small">
                      <Image
                        src={results.monthly_chart_url}
                        alt="Monthly Returns"
                        style={{ width: '100%' }}
                      />
                    </Card>
                  </Col>
                )}
                
                {results.drawdown_chart_url && (
                  <Col xs={24}>
                    <Card title="Drawdown Analysis" size="small">
                      <Image
                        src={results.drawdown_chart_url}
                        alt="Drawdown Analysis"
                        style={{ width: '100%' }}
                      />
                    </Card>
                  </Col>
                )}
              </Row>
            </>
          )}
        </Card>
      </div>
    </div>
  )
}

export default ResultsPage