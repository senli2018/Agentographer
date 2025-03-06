import axios from 'axios';
import { message } from 'ant-design-vue';

// Markdown to pure text utility function
function markdownToText(markdown) {
    if (!markdown) return '';
    
    return markdown
        // Remove bold
        .replace(/\*\*(.*?)\*\*/g, '$1')
        // Remove italic
        .replace(/\*(.*?)\*/g, '$1')
        .replace(/_(.*?)_/g, '$1')
        // Remove code blocks
        .replace(/```[\s\S]*?```/g, '')
        // Remove inline code
        .replace(/`(.*?)`/g, '$1')
        // Remove titles
        .replace(/#{1,6}\s/g, '')
        // Remove links
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$1')
        // Remove images
        .replace(/!\[([^\]]+)\]\(([^)]+)\)/g, '')
        // Remove quotes
        .replace(/^\s*>\s/gm, '')
        // Remove horizontal rules
        .replace(/^-{3,}|_{3,}|\*{3,}$/gm, '')
        // Remove list markers
        .replace(/^[\*\-+]\s/gm, '')
        .replace(/^\d+\.\s/gm, '')
        // Clean up extra spaces and newlines
        .replace(/\n{3,}/g, '\n\n')
        .trim();
}

//1. Create axios object
const service = axios.create({
    baseURL: '/',
    timeout: 200000,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: false  // Change to false
});

//2. Request interceptor
service.interceptors.request.use(config => {
    console.log('Sending request:', config.url, config.data);
    return config;
}, error => {
    console.error('Request error:', error);
    message.error('Request failed');
    return Promise.reject(error);
});

//3. Response interceptor
service.interceptors.response.use(response => {
    console.log('Received response:', response.data);
    const res = response.data;
    
    // If response is a string, return directly
    if (typeof res === 'string') {
        return {
            code: 200,
            data: {
                message: markdownToText(res)
            }
        };
    }
    
    // If there is no code field, it is considered direct data
    if (res.code === undefined) {
        return {
            code: 200,
            data: {
                message: markdownToText(res.message || res)
            }
        };
    }

    if (res.code !== 200) {
        const errMsg = res.message || 'Request failed';
        message.error(errMsg);
        return Promise.reject(new Error(errMsg));
    }

    // Process normal responses
    if (res.data && res.data.message) {
        res.data.message = markdownToText(res.data.message);
    }
    return res;
}, error => {
    console.error('Response error:', error);
    if (error.code === 'ECONNABORTED') {
        message.error('Request timeout, please check the network');
    } else if (error.response) {
        switch (error.response.status) {
            case 401:
                message.error('Unauthorized, please log in again');
                break;
            case 403:
                message.error('Access denied');
                break;
            case 404:
                message.error('The requested resource does not exist');
                break;
            case 500:
                message.error('Server internal error');
                break;
            default:
                message.error(`Request failed: ${error.response.status}`);
        }
    } else if (error.request) {
        message.error('Server not responding, please check the network connection');
        console.error('Request sent successfully but no response:', error.request);
    } else {
        message.error('Request configuration error');
        console.error('Request configuration error:', error.message);
    }
    return Promise.reject(error);
});

export default service;
