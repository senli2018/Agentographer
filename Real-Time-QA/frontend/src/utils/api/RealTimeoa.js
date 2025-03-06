import request from '@/utils/request'
import { message } from 'ant-design-vue'

export function Disconnect (data) {
    if (!data) {
        message.error('Missing client id');
        return Promise.reject(new Error('The client id is empty'));
    }

    return request({
        url: `/api/ws/disconnect/${data}`,
        method: 'post',
  
        timeout: 200000  
    }).catch(error => {
        console.error('Chat request failed:', error);
        throw error;
    });
}
