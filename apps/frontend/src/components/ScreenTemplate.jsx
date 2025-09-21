import React from 'react';

function ScreenTemplate({ children, title = "Life Abroad" }) {
  return (
    <div className="screen-template">
      <header className="screen-header">
        <div className="header-container">
          <h1 className="screen-title">{title}</h1>
          <div className="header-pills">
            <div className="header-pill pill-1"></div>
            <div className="header-pill pill-2"></div>
            <div className="header-pill pill-3"></div>
          </div>
        </div>
      </header>
      
      <main className="screen-main">
        {children}
      </main>
    </div>
  );
}

export default ScreenTemplate;