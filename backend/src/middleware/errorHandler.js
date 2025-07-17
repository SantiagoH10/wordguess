const errorHandler = (err, req, res, next) => {
  console.error(err.stack)

  // Handle validation errors
  if (err.message.includes('Invalid')) {
    return res.status(400).json({
      error: {
        message: err.message,
        type: 'ValidationError',
      },
    })
  }

  // Handle Python script errors
  if (err.message.includes('Python')) {
    return res.status(500).json({
      error: {
        message: 'ML service error',
        type: 'MLServiceError',
        ...(process.env.NODE_ENV === 'development' && { details: err.message }),
      },
    })
  }

  // Default error
  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal Server Error',
      type: 'ServerError',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    },
  })
}

export default errorHandler
