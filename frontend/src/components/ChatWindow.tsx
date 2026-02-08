import React, { useState, useEffect, useRef } from 'react';
import { Channel, Message, WebSocketMessage } from '../types';
import { messageAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import websocketService from '../services/websocket';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatWindow.css';

interface ChatWindowProps {
  channel: Channel;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ channel }) => {
  const { token, user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadMessages();
    connectWebSocket();

    return () => {
      websocketService.disconnect();
    };
  }, [channel.id]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadMessages = async () => {
    setLoading(true);
    try {
      const data = await messageAPI.getMessages(channel.id);
      setMessages(data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    if (!token) return;

    websocketService.connect(
      channel.id,
      token,
      handleWebSocketMessage,
      () => setConnected(true),
      () => setConnected(false)
    );
  };

  const handleWebSocketMessage = (wsMessage: WebSocketMessage) => {
    if (wsMessage.type === 'message') {
      const newMessage: Message = {
        id: wsMessage.id!,
        content: wsMessage.content,
        user_id: wsMessage.user_id!,
        username: wsMessage.username,
        channel_id: wsMessage.channel_id,
        created_at: wsMessage.timestamp,
      };
      setMessages((prev) => [...prev, newMessage]);
    }
  };

  const handleSendMessage = (content: string) => {
    websocketService.sendMessage(content);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-header-info">
          <h2>#{channel.name}</h2>
          {channel.description && <p>{channel.description}</p>}
        </div>
        <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </div>

      <div className="chat-messages">
        {loading ? (
          <div className="loading-messages">Loading messages...</div>
        ) : (
          <>
            <MessageList messages={messages} currentUserId={user?.id} />
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <MessageInput onSend={handleSendMessage} disabled={!connected} />
    </div>
  );
};

export default ChatWindow;
