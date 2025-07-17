import { spawn } from 'child_process'

class PythonRunner {
  static async runScript(scriptPath, args = []) {
    return new Promise((resolve, reject) => {
      const python = spawn('../ml-service/venv/bin/python', [
        '../ml-service/scripts/word2vec_cli.py',
        ...args,
      ])

      let result = ''
      let error = ''

      python.stdout.on('data', data => {
        result += data.toString()
      })

      python.stderr.on('data', data => {
        error += data.toString()
      })

      python.on('close', code => {
        if (code !== 0) {
          reject(new Error(`Python script failed: ${error}`))
        } else {
          try {
            resolve(JSON.parse(result))
          } catch (e) {
            reject(new Error(`Invalid JSON response: ${result}`))
          }
        }
      })

      python.on('error', err => {
        reject(new Error(`Failed to start Python process: ${err.message}`))
      })
    })
  }
}

export default PythonRunner
