import express from "express"
import cors from "cors"
import cookieParser from "cookie-parser"
import morgan from "morgan"
import dotenv from "dotenv"
dotenv.config();

const app = express();

// 1. Define the list of allowed URLs
const allowedOrigins = [
  process.env.CLIENT_URL,
  'http://localhost:5173'
];

// 2. Update CORS to check the list
app.use(cors({
    origin: function (origin, callback) {
      // Allow requests with no origin (like Postman) or if the origin is in our list
      if (!origin || allowedOrigins.indexOf(origin) !== -1) {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    },
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
    exposedHeaders: ['Content-Range', 'X-Content-Range'],
    maxAge: 86400 // 24 hours
}));

app.use(cookieParser());

// Only parse JSON and urlencoded, NOT multipart - multer handles that
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(morgan('dev'));

// Handle preflight requests
app.options('*', cors());

export { app };