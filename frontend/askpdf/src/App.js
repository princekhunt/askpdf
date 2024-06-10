import { useEffect } from "react";

import { Routes, Route } from "react-router-dom";
import Root from "./pages/Root";

function App() {
  //clear the session on refresh
  useEffect(() => {
    localStorage.clear();
  }, []);

  return (
    <Routes>
      <Route path="/" element={<Root />} />
    </Routes>
  );
}

export default App;
