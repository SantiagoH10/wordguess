import cors from 'cors'

const corsOptions = {
  origin: '*', // Allow all origins
  credentials: false, // Must be false when origin is '*'
  optionsSuccessStatus: 200,
}

export default cors(corsOptions)
