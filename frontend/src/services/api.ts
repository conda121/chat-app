import axios from 'axios';
import { LoginCredentials, RegisterData, AuthResponse, User, Channel, Message } from '../types';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

export const channelAPI = {
  getChannels: async (): Promise<Channel[]> => {
    const response = await api.get('/channels/');
    return response.data;
  },

  createChannel: async (name: string, description?: string): Promise<Channel> => {
    const response = await api.post('/channels/', { name, description });
    return response.data;
  },

  joinChannel: async (channelId: number): Promise<Channel> => {
    const response = await api.post(`/channels/${channelId}/join`);
    return response.data;
  },

  leaveChannel: async (channelId: number): Promise<void> => {
    await api.post(`/channels/${channelId}/leave`);
  },
};

export const messageAPI = {
  getMessages: async (channelId: number, limit = 50): Promise<Message[]> => {
    const response = await api.get(`/channels/${channelId}/messages`, {
      params: { limit },
    });
    return response.data;
  },
};

export default api;
