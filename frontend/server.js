/**
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the dist directory
const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));

import fs from 'fs';

// Handle React Router SPA routing: send all unmatched requests to index.html with injected VITE_API_URL
app.get('/{*splat}', (req, res) => {
  const indexPath = path.join(distPath, 'index.html');
  try {
    let html = fs.readFileSync(indexPath, 'utf-8');
    const apiUrl = process.env.VITE_API_URL || 'http://localhost:8080';
    // Inject the variable into the head tag
    html = html.replace('</head>', `<script>window.VITE_API_URL="${apiUrl}"</script></head>`);
    res.send(html);
  } catch (err) {
    res.status(500).send("Internal Server Error: Unable to read index.html");
  }
});

app.listen(PORT, () => {
  console.log(`Frontend server is running on port ${PORT}`);
});
