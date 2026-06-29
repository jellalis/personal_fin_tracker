import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import { Dashboard } from "./Dashboard";
import { Login } from "./Login";
import { isLoggedIn, clearToken } from "./api";
import "./styles.css";

function App() {
  // Track login state — re-renders when user logs in or out
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

  if (!loggedIn) {
    // Not logged in → show login screen
    // onLogin is called by Login component after successful token save
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  // Logged in → show dashboard with a logout button
  return (
    <Dashboard
      onLogout={() => {
        clearToken();          // remove JWT from localStorage
        setLoggedIn(false);    // re-render → shows Login screen
      }}
    />
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
