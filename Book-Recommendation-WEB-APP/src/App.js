import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RecommendationForm from "./Components/RecommendationForm";
import RecommendationTable from "./Components/RecommendationTable";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RecommendationForm />} />
        <Route path="/recommendations" element={<RecommendationTable />} />
      </Routes>
    </Router>
  );
}

export default App;
