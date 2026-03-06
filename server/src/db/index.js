import mongoose from "mongoose";
import { DB_NAME } from "../constant.js";
import dotenv from "dotenv"

dotenv.config();

const connectDB = async () => {
    try {
        const options = {
            serverSelectionTimeoutMS: 5000,
            socketTimeoutMS: 45000,
        };
        
        const connectionInstance = await mongoose.connect(`${process.env.MONGODB_URL}/${DB_NAME}`, options);
        console.log(`✅ MongoDB connected at host: ${connectionInstance.connection.host}`);
        return connectionInstance;
    } catch (error) {
        console.error(`❌ MongoDB Connection Error: ${error.message}`);
        console.error('⚠️  Server starting without database. Some features may not work.');
        // Don't exit - let server start anyway
        return null;
    }
}
export default connectDB;

