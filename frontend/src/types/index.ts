export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  last_seen: string;
}

export interface Channel {
  id: number;
  name: string;
  description?: string;
  created_by: number;
  created_at: string;
}

export interface Message {
  id: number;
  content: string;
  user_id: number;
  username: string;
  channel_id: number;
  created_at: string;
}

export interface WebSocketMessage {
  type: 'message' | 'user_joined' | 'user_left';
  id?: number;
  content: string;
  username: string;
  user_id?: number;
  channel_id: number;
  timestamp: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
