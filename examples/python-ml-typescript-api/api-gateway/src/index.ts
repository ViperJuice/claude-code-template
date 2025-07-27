import express, { Request, Response } from 'express';
import cors from 'cors';
import axios from 'axios';
import rateLimit from 'express-rate-limit';
import NodeCache from 'node-cache';

const app = express();
const cache = new NodeCache({ stdTTL: 600 }); // 10 minute cache
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8003';

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});

app.use('/api/', limiter);

// Types
interface SentimentRequest {
  text: string;
}

interface BatchSentimentRequest {
  texts: string[];
}

interface SentimentResponse {
  text: string;
  sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
  timestamp: string;
}

// Health check
app.get('/health', async (req: Request, res: Response) => {
  try {
    const mlHealth = await axios.get(`${ML_SERVICE_URL}/health`);
    res.json({
      status: 'healthy',
      services: {
        api_gateway: 'healthy',
        ml_service: mlHealth.data.status
      }
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: 'ML service unavailable'
    });
  }
});

// Single text analysis
app.post('/api/analyze', async (req: Request<{}, {}, SentimentRequest>, res: Response) => {
  try {
    const { text } = req.body;
    
    if (!text || text.trim().length === 0) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Check cache
    const cacheKey = `sentiment:${text}`;
    const cachedResult = cache.get<SentimentResponse>(cacheKey);
    if (cachedResult) {
      return res.json({ ...cachedResult, cached: true });
    }

    // Call ML service
    const response = await axios.post(`${ML_SERVICE_URL}/analyze`, { text });
    const result = response.data;
    
    // Cache the result
    cache.set(cacheKey, result);
    
    res.json(result);
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    res.status(500).json({ error: 'Failed to analyze sentiment' });
  }
});

// Batch text analysis
app.post('/api/batch-analyze', async (req: Request<{}, {}, BatchSentimentRequest>, res: Response) => {
  try {
    const { texts } = req.body;
    
    if (!texts || !Array.isArray(texts) || texts.length === 0) {
      return res.status(400).json({ error: 'Texts array is required' });
    }

    if (texts.length > 100) {
      return res.status(400).json({ error: 'Maximum 100 texts allowed per batch' });
    }

    // Call ML service
    const response = await axios.post(`${ML_SERVICE_URL}/batch-analyze`, { texts });
    res.json(response.data);
  } catch (error) {
    console.error('Error in batch analysis:', error);
    res.status(500).json({ error: 'Failed to analyze batch' });
  }
});

// Model information
app.get('/api/model/info', async (req: Request, res: Response) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/model/info`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get model info' });
  }
});

// API documentation
app.get('/api', (req: Request, res: Response) => {
  res.json({
    version: '1.0.0',
    endpoints: {
      'POST /api/analyze': 'Analyze sentiment of a single text',
      'POST /api/batch-analyze': 'Analyze sentiment of multiple texts',
      'GET /api/model/info': 'Get information about the ML model',
      'GET /health': 'Health check endpoint'
    }
  });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`API Gateway running on http://localhost:${PORT}`);
});