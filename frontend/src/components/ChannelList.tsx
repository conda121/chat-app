import React from 'react';
import { Channel } from '../types';
import './ChannelList.css';

interface ChannelListProps {
  channels: Channel[];
  selectedChannel: Channel | null;
  onSelectChannel: (channel: Channel) => void;
  onCreateChannel: () => void;
}

const ChannelList: React.FC<ChannelListProps> = ({
  channels,
  selectedChannel,
  onSelectChannel,
  onCreateChannel,
}) => {
  return (
    <div className="channel-list">
      <div className="channel-list-header">
        <h3>Channels</h3>
        <button onClick={onCreateChannel} className="btn-add-channel" title="Create Channel">
          +
        </button>
      </div>

      <div className="channel-items">
        {channels.length === 0 ? (
          <div className="no-channels">
            <p>No channels yet</p>
            <small>Create one to get started!</small>
          </div>
        ) : (
          channels.map((channel) => (
            <div
              key={channel.id}
              className={`channel-item ${selectedChannel?.id === channel.id ? 'active' : ''}`}
              onClick={() => onSelectChannel(channel)}
            >
              <div className="channel-icon">#</div>
              <div className="channel-info">
                <div className="channel-name">{channel.name}</div>
                {channel.description && (
                  <div className="channel-description">{channel.description}</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ChannelList;
