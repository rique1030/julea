import { HashRouter as Router, Routes, Route } from "react-router-dom";
import "./rose-pine.css";
import "./App.css";
import "material-icons/iconfont/material-icons.css";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import {
  apiReducer,
  outputReducer,
  webselectionReducer,
  searchMethodReducer,
  automationStateReducer,
  progressInfoReducer,
} from "@src/store";

import WelcomePage from "./pages/welcome/index.jsx";
import ControllerPage from "./pages/controller/index.jsx";

const store = configureStore({
  reducer: {
    api: apiReducer,
    output: outputReducer,
    webselection: webselectionReducer,
    searchmethod: searchMethodReducer,
    automation: automationStateReducer,
    progress: progressInfoReducer,
  },
});

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="App">
              <WelcomePage />
            </div>
          }
        />
        <Route
          path="/controller"
          element={
            <div className="App">
              <ControllerPage />
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

function AppWithStore() {
  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}

export default AppWithStore;
