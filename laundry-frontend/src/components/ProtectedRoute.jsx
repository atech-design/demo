// src/components/ProtectedRoute.jsx
import { Navigate, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";

export default function ProtectedRoute({ children, adminOnly = false }) {
  const user = useSelector((state) => state.auth.user);
  const location = useLocation();

  if (!user) {
    // Not logged in → redirect to login with return path
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (adminOnly && !user.is_staff) {
    // Logged in but not admin → redirect to services
    return <Navigate to="/services" replace />;
  }

  return children;
}
