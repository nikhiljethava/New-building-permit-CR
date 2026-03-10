FROM node:20-alpine
WORKDIR /app

# Copy package files and install all dependencies (including devDependencies for the build)
COPY package*.json ./
RUN npm install

# Copy source code and build the React application
COPY . .
RUN npm run build

# Expose port 3000 (which server.js uses by default)
EXPOSE 3000

# Start the Express server
CMD ["node", "server.js"]
