import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { channelAPI } from '../services/api';
import { Channel } from '../types';
import ChannelList from '../components/ChannelList';
import ChatWindow from '../components/ChatWindow';
import CreateChannel from '../components/CreateChannel';
import './Chat.css';

const Chat: React.FC = () => {
  const { user, logout } = useAuth();
  const [channels, setChannels] = useState<Channel[]>([]);
  const [selectedChannel, setSelectedChannel] = useState<Channel | null>(null);
  const [showCreateChannel, setShowCreateChannel] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChannels();
  }, []);

  const loadChannels = async () => {
    try {
      const data = await channelAPI.getChannels();
      setChannels(data);
      if (data.length > 0 && !selectedChannel) {
        setSelectedChannel(data[0]);
      }
    } catch (error) {
      console.error('Failed to load channels:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChannelCreated = (channel: Channel) => {
    setChannels([...channels, channel]);
    setSelectedChannel(channel);
    setShowCreateChannel(false);
  };

  return (
    <div className="chat-container">
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Chat App</h2>
          <div className="user-info">
            <span>👤 {user?.username}</span>
            <button onClick={logout} className="btn-logout">Logout</button>
          </div>
        </div>

        <ChannelList
          channels={channels}
          selectedChannel={selectedChannel}
          onSelectChannel={setSelectedChannel}
          onCreateChannel={() => setShowCreateChannel(true)}
        />
      </div>

      <div className="main-content">
        {selectedChannel ? (
          <ChatWindow channel={selectedChannel} />
        ) : (
          <div className="no-channel-selected">
            <h2>Welcome to Chat App!</h2>
            <p>Select a channel to start chatting</p>
          </div>
        )}
      </div>

      {showCreateChannel && (
        <CreateChannel
          onClose={() => setShowCreateChannel(false)}
          onCreated={handleChannelCreated}
        />
      )}
    </div>
  );
};

export default Chat;
