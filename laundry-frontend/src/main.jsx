import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

// 🔑 Redux setup
import { Provider } from "react-redux";
import store from "./store/store";

// 🌐 i18n setup import (zaroori hai for multi-language)
import "./i18n";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
