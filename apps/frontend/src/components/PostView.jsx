import React from 'react';

function PostView({ post }) {
  const handleViewAllPosts = () => {
    // Remove post_id from URL to show all posts
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.delete('post_id');
    window.location.search = urlParams.toString();
  };

  return (
    <div className="post-view">
      <div className="post-header">
        <button 
          className="view-all-button"
          onClick={handleViewAllPosts}
        >
          view all {post.creator_name}'s posts
        </button>
      </div>
      
      <div className="post-content">
        <div className="post-info">
          <p className="post-description">{post.description}</p>
          <p className="post-date">{new Date(post.created_at).toLocaleDateString()}</p>
        </div>
        
        {post.media_items && post.media_items.length > 0 && (
          <div className="media-gallery">
            <h3>Media ({post.media_items.length} items)</h3>
            <div className="media-grid">
              {post.media_items.map((media) => {
                console.log('Rendering media item:', media); // Debug
                return (
                  <div key={media.id} className="media-item">
                    {media.url ? (
                      media.type === 'photo' || media.type === 'image' ? (
                        <img 
                          src={media.url} 
                          alt="Post media"
                          className="media-image"
                          onLoad={() => console.log('Image loaded successfully')}
                          onError={(e) => {
                            console.error('Image failed to load:', media.url);
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'block';
                          }}
                        />
                      ) : media.type === 'video' ? (
                        <video 
                          src={media.url} 
                          controls
                          className="media-video"
                          onLoadedData={() => console.log('Video loaded successfully')}
                          onError={(e) => {
                            console.error('Video failed to load:', media.url);
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'block';
                          }}
                        />
                      ) : (
                        <div className="media-placeholder">
                          {media.type} file
                        </div>
                      )
                    ) : (
                      <div className="media-error">
                        Failed to load {media.type}
                      </div>
                    )}
                    {media.url && (
                      <div className="media-error" style={{display: 'none'}}>
                        Failed to load {media.type}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PostView;