FROM node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy all other frontend files
COPY . .

EXPOSE 5173

# Run the dev server
CMD ["npm", "run", "dev"]
