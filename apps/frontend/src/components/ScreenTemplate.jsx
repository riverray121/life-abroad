import React from 'react';

function ScreenTemplate({ children, title = "Life Abroad" }) {
  return (
    <div className="screen-template">
      <header className="screen-header">
        <h1 className="screen-title">{title}</h1>
      </header>
      
      <main className="screen-main">
        {children}
      </main>
    </div>
  );
}

export default ScreenTemplate;