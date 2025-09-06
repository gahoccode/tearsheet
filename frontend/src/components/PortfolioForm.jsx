import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import dayjs from 'dayjs'
import { 
  Form, 
  Input, 
  InputNumber, 
  DatePicker, 
  Button, 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space,
  message,
  Spin
} from 'antd'
import { BarChartOutlined } from '@ant-design/icons'

const { Title } = Typography

function PortfolioForm() {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const onFinish = async (values) => {
    setLoading(true)
    try {
      // Transform form data to match Flask backend expectations
      const formData = new FormData()
      
      // Add symbols and weights as arrays
      values.portfolio.forEach(item => {
        formData.append('symbols[]', item.symbol)
        formData.append('weights[]', item.weight)
      })
      
      // Add dates and capital
      formData.append('start_date', values.start_date.format('YYYY-MM-DD'))
      formData.append('end_date', values.end_date.format('YYYY-MM-DD'))
      formData.append('capital', values.capital)

      const response = await axios.post('/analyze', formData, {
        headers: {
          'Accept': 'application/json'
        }
      })
      
      if (response.status === 200 && response.data.success) {
        // Navigate to results page
        navigate('/results')
        message.success('Analysis completed successfully!')
      }
    } catch (error) {
      console.error('Analysis failed:', error)
      message.error('Analysis failed. Please check your inputs and try again.')
    } finally {
      setLoading(false)
    }
  }

  const validateWeights = (_, value) => {
    const portfolio = form.getFieldValue('portfolio') || []
    const totalWeight = portfolio.reduce((sum, item) => sum + (item?.weight || 0), 0)
    
    if (Math.abs(totalWeight - 1.0) > 0.001) {
      return Promise.reject(new Error('Portfolio weights must sum to 1.0'))
    }
    return Promise.resolve()
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f8f9fa', 
      padding: '40px 24px' 
    }}>
      <div style={{ maxWidth: 700, margin: '0 auto' }}>
        <Card>
          <Title level={1} style={{ textAlign: 'center', marginBottom: 32 }}>
            <BarChartOutlined style={{ marginRight: 12 }} />
            Vietnam Stock Portfolio Analyzer
          </Title>

          <Form
            form={form}
            layout="vertical"
            onFinish={onFinish}
            initialValues={{
              portfolio: [
                { symbol: 'REE', weight: 0.7 },
                { symbol: 'FMC', weight: 0.2 },
                { symbol: 'DHC', weight: 0.1 }
              ],
              start_date: dayjs('2023-01-01'),
              end_date: dayjs('2025-04-15'),
              capital: 500000000
            }}
          >
            <Title level={3}>Portfolio Composition</Title>
            
            <Form.List name="portfolio">
              {(fields) => (
                <>
                  {fields.map((field, index) => (
                    <Row gutter={16} key={field.key}>
                      <Col span={12}>
                        <Form.Item
                          {...field}
                          label={`Symbol ${index + 1}`}
                          name={[field.name, 'symbol']}
                          rules={[{ required: true, message: 'Please enter symbol' }]}
                        >
                          <Input placeholder="e.g. REE" />
                        </Form.Item>
                      </Col>
                      <Col span={12}>
                        <Form.Item
                          {...field}
                          label="Weight"
                          name={[field.name, 'weight']}
                          rules={[
                            { required: true, message: 'Please enter weight' },
                            { type: 'number', min: 0, max: 1, message: 'Weight must be between 0 and 1' },
                            { validator: validateWeights }
                          ]}
                        >
                          <InputNumber 
                            style={{ width: '100%' }} 
                            min={0} 
                            max={1} 
                            step={0.01} 
                            placeholder="0.00"
                          />
                        </Form.Item>
                      </Col>
                    </Row>
                  ))}
                </>
              )}
            </Form.List>

            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  label="Start Date"
                  name="start_date"
                  rules={[{ required: true, message: 'Please select start date' }]}
                >
                  <DatePicker style={{ width: '100%' }} />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  label="End Date" 
                  name="end_date"
                  rules={[{ required: true, message: 'Please select end date' }]}
                >
                  <DatePicker style={{ width: '100%' }} />
                </Form.Item>
              </Col>
            </Row>

            <Form.Item
              label="Initial Capital (VND)"
              name="capital"
              rules={[
                { required: true, message: 'Please enter initial capital' },
                { type: 'number', min: 1000000, message: 'Minimum capital is 1,000,000 VND' }
              ]}
            >
              <InputNumber 
                style={{ width: '100%' }}
                min={1000000}
                step={100000}
                formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>

            <Form.Item>
              <Button 
                type="primary" 
                htmlType="submit" 
                size="large"
                loading={loading}
                block
              >
                {loading ? 'Analyzing Portfolio...' : 'Analyze Portfolio'}
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>
    </div>
  )
}

export default PortfolioForm