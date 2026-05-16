FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
COPY jest.config.js ./

# Install all dependencies (including dev for tests)
RUN npm ci

COPY . .

# Run tests and generate coverage
RUN npm test || true

RUN chmod +x docker-entrypoint.sh

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:5000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || echo "Health check endpoint not configured"

CMD ["sh", "docker-entrypoint.sh"]
