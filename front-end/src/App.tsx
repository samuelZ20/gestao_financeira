import { Routes, Route } from "react-router-dom";
import Hello from "./pages/Hello";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Hello />} />
    </Routes>
  );
}