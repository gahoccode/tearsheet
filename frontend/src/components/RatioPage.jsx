import { useState } from 'react'
import axios from 'axios'
import { 
  Form, 
  Input, 
  Select, 
  Button, 
  Card, 
  Row, 
  Col, 
  Typography, 
  Table,
  message,
  Spin,
  Alert,
  Layout,
  Space
} from 'antd'
import { BarChartOutlined, HomeOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Title, Text } = Typography
const { Option } = Select
const { Content } = Layout

function RatioPage() {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [ratioData, setRatioData] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const onFinish = async (values) => {
    setLoading(true)
    setError(null)
    setRatioData(null)
    
    try {
      const formData = new FormData()
      formData.append('stock_symbol', values.stock_symbol.toUpperCase())
      formData.append('period', values.period)

      const response = await axios.post('/ratio/analyze', formData, {
        headers: {
          'Accept': 'application/json'
        }
      })

      if (response.data.success) {
        setRatioData(response.data)
        message.success(`Financial ratios loaded successfully for ${response.data.stock_symbol}`)
      } else {
        setError(response.data.error)
        message.error(response.data.error)
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to fetch financial ratios'
      setError(errorMsg)
      message.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // Prepare table columns dynamically
  const getTableColumns = () => {
    if (!ratioData || !ratioData.columns) return []
    
    return ratioData.columns.map(col => ({
      title: col.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      dataIndex: col,
      key: col,
      render: (value) => {
        // Format numeric values
        if (typeof value === 'number') {
          return value.toFixed(4)
        }
        return value || '-'
      }
    }))
  }

  // Prepare table data
  const getTableData = () => {
    if (!ratioData || !ratioData.ratio_data) return []
    
    return ratioData.ratio_data.map((row, index) => ({
      ...row,
      key: index
    }))
  }

  return (
    <Layout style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      <Content style={{ padding: '40px 24px' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          {/* Header */}
          <Space direction="vertical" size="large" style={{ width: '100%', marginBottom: 32 }}>
            <Card>
              <Space size="large" style={{ width: '100%', justifyContent: 'space-between' }}>
                <Space align="center">
                  <BarChartOutlined style={{ fontSize: 24, color: '#1a237e' }} />
                  <Title level={2} style={{ margin: 0 }}>Financial Ratios Analysis</Title>
                </Space>
                <Button 
                  icon={<HomeOutlined />} 
                  onClick={() => navigate('/')}
                >
                  Portfolio Analysis
                </Button>
              </Space>
              <Text style={{ color: '#666', display: 'block', marginTop: 8 }}>
                Analyze financial ratios for Vietnam stock market companies using real-time data
              </Text>
            </Card>
          </Space>

          {/* Input Form */}
          <Card style={{ marginBottom: 24 }}>
            <Form
              form={form}
              layout="vertical"
              onFinish={onFinish}
              initialValues={{
                period: 'year'
              }}
            >
              <Row gutter={16}>
                <Col xs={24} sm={12} md={8}>
                  <Form.Item
                    label="Stock Symbol"
                    name="stock_symbol"
                    rules={[
                      { required: true, message: 'Please enter a stock symbol!' },
                      { pattern: /^[A-Za-z]{3,4}$/, message: 'Enter a valid stock symbol (3-4 letters)' }
                    ]}
                  >
                    <Input 
                      placeholder="e.g., REE, VIC, FMC" 
                      style={{ textTransform: 'uppercase' }}
                    />
                  </Form.Item>
                </Col>
                
                <Col xs={24} sm={12} md={8}>
                  <Form.Item
                    label="Period"
                    name="period"
                  >
                    <Select>
                      <Option value="year">Annual</Option>
                      <Option value="quarter">Quarterly</Option>
                    </Select>
                  </Form.Item>
                </Col>
                
                <Col xs={24} sm={24} md={8}>
                  <Form.Item label=" " style={{ marginBottom: 0 }}>
                    <Button 
                      type="primary" 
                      htmlType="submit" 
                      loading={loading}
                      icon={<BarChartOutlined />}
                      block
                      style={{ height: 40 }}
                    >
                      {loading ? 'Analyzing...' : 'Get Financial Ratios'}
                    </Button>
                  </Form.Item>
                </Col>
              </Row>
            </Form>
          </Card>

          {/* Error Display */}
          {error && (
            <Alert
              message="Error"
              description={error}
              type="error"
              showIcon
              style={{ marginBottom: 24 }}
            />
          )}

          {/* Loading Spinner */}
          {loading && (
            <Card style={{ textAlign: 'center' }}>
              <Space direction="vertical" align="center">
                <Spin size="large" />
                <Text>Fetching financial ratios data...</Text>
              </Space>
            </Card>
          )}

          {/* Results Table */}
          {ratioData && !loading && (
            <Card>
              <Space direction="vertical" size="small" style={{ marginBottom: 16 }}>
                <Title level={3} style={{ margin: 0 }}>
                  Financial Ratios - {ratioData.stock_symbol}
                </Title>
                <Text style={{ color: '#666' }}>
                  Period: {ratioData.period === 'year' ? 'Annual' : 'Quarterly'} | 
                  Records: {ratioData.ratio_data.length}
                </Text>
              </Space>
              
              <Table
                columns={getTableColumns()}
                dataSource={getTableData()}
                scroll={{ x: true }}
                pagination={{
                  showSizeChanger: true,
                  showQuickJumper: true,
                  showTotal: (total, range) => 
                    `${range[0]}-${range[1]} of ${total} records`
                }}
                size="middle"
              />
            </Card>
          )}

          {/* Help Section */}
          {!ratioData && !loading && (
            <Card style={{ backgroundColor: '#f0f8ff', borderColor: '#1890ff' }}>
              <Title level={4} style={{ color: '#1a237e' }}>How to use:</Title>
              <ul style={{ color: '#1a237e', margin: 0 }}>
                <li>• Enter a valid Vietnam stock symbol (e.g., REE, VIC, FMC, DHC)</li>
                <li>• Choose between Annual or Quarterly data</li>
                <li>• Click "Get Financial Ratios" to fetch the data</li>
                <li>• View comprehensive financial ratios in the table below</li>
              </ul>
            </Card>
          )}
        </div>
      </Content>
    </Layout>
  )
}

export default RatioPage