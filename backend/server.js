import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import word2vecRoutes from './routes/word2vec.js';
import indexRoutes from './routes/index.js';
import errorHandler from './middleware/errorHandler.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/word2vec', word2vecRoutes);
app.use('/api', indexRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Error handling middleware (should be last)
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
