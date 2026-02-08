import React from 'react';
import { Message } from '../types';
import './MessageList.css';

interface MessageListProps {
  messages: Message[];
  currentUserId?: number;
}

const MessageList: React.FC<MessageListProps> = ({ messages, currentUserId }) => {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      });
    }
  };

  let lastDate = '';

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="no-messages">
          <p>No messages yet</p>
          <small>Be the first to send a message!</small>
        </div>
      ) : (
        messages.map((message, index) => {
          const messageDate = formatDate(message.created_at);
          const showDateSeparator = messageDate !== lastDate;
          lastDate = messageDate;

          return (
            <React.Fragment key={message.id}>
              {showDateSeparator && (
                <div className="date-separator">
                  <span>{messageDate}</span>
                </div>
              )}
              
              <div className={`message ${message.user_id === currentUserId ? 'own-message' : ''}`}>
                <div className="message-avatar">
                  {message.username.charAt(0).toUpperCase()}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-username">{message.username}</span>
                    <span className="message-time">{formatTime(message.created_at)}</span>
                  </div>
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            </React.Fragment>
          );
        })
      )}
    </div>
  );
};

export default MessageList;
