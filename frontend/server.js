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
import { GoogleAuth } from 'google-auth-library';

const auth = new GoogleAuth();
let cachedToken = null;
let tokenExpiry = 0;

async function getAccessToken() {
    if (cachedToken && Date.now() < tokenExpiry) {
        return cachedToken;
    }
    try {
        const client = await auth.getClient();
        const token = await client.getAccessToken();
        cachedToken = token.token;
        tokenExpiry = Date.now() + 50 * 60 * 1000;
        return cachedToken;
    } catch (e) {
        console.error("Failed to get access token:", e);
        return null;
    }
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

import { createProxyMiddleware } from 'http-proxy-middleware';
const apiBackendUrl = process.env.API_BACKEND_SERVICE_URL || 'http://localhost:8080';

// Proxy API requests to backend
// Strip trailing /api to avoid double-up with pathFilter if they pass it with /api
app.use(createProxyMiddleware({
    pathFilter: '/api',
    target: apiBackendUrl.replace(/\/api$/, ''),
    changeOrigin: true,
}));

// Proxy OTel traces to Telemetry API
app.use('/v1/traces', async (req, res, next) => {
    const token = await getAccessToken();
    if (token) {
        req.headers['authorization'] = `Bearer ${token}`;
        if (process.env.VITE_PROJECT_ID) {
            req.headers['x-goog-user-project'] = process.env.VITE_PROJECT_ID;
        }
    }
    next();
});

app.use(createProxyMiddleware({
    pathFilter: '/v1/traces',
    target: 'https://telemetry.googleapis.com',
    changeOrigin: true,
}));

// Serve static files from the dist directory
const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath, { index: false }));

import fs from 'fs';

// Handle React Router SPA routing: send all unmatched requests to index.html
app.get(/.*$/, (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Frontend server is running on port ${PORT}`);
});
