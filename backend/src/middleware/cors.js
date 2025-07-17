import cors from 'cors'

const corsOptions = {
  origin: '*',
  credentials: false,
  optionsSuccessStatus: 200,
}

export default cors(corsOptions)
