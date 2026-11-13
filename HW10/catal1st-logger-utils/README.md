# catal1st-logger-utils

A simple, lightweight, and structured terminal logging utility for Node.js projects. This package helps developers replace standard console logs with clear, categorized terminal outputs to improve readability during development and debugging.

## Features

- Clear categorical prefixes for different log types.
- Zero external dependencies.
- Lightweight and easy to integrate into any existing Node.js project.

## Installation

Install the package into your project directory using npm:

```bash
npm install catal1st-logger-utils
```

## Quick Start Usage

Import the package into your JavaScript file and call the available logging methods:

```javascript
const logger = require("catal1st-logger-utils");

// General information logging
logger.logInfo("System initialization started...");

// Success state logging
logger.logSuccess("Database connected successfully!");

// Error state logging
logger.logError("Failed to fetch data from the server.");
```

## API Reference

The package exports an object containing three primary logging functions:

### `logInfo(message)`

Outputs a standard informational message to the console.

- **Parameters:** `message` (String) - The text to be logged.
- **Console Output Format:** `[INFO] {message}`

### `logSuccess(message)`

Outputs a success message to the console to indicate a completed task or successful operation.

- **Parameters:** `message` (String) - The text to be logged.
- **Console Output Format:** `[SUCCESS] {message}`

### `logError(message)`

Outputs an error message to the console using the standard error stream.

- **Parameters:** `message` (String) - The error description to be logged.
- **Console Output Format:** `[ERROR] {message}`

## License

This project is licensed under the MIT License.

## Author

Created and maintained by Samuel Audric Raphael (CataL1st).
