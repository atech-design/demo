import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loginUser, setUserFromToken } from "../slices/authSlice";
import { useNavigate, useLocation } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";
import api from "../api";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

export default function Login() {
  const [formData, setFormData] = useState({ email: "" });
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const otpInputRef = useRef(null);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  // Auto-login if token exists
  useEffect(() => {
    const tokenData = localStorage.getItem("smartLaundryUser");
    if (tokenData) {
      const parsed = JSON.parse(tokenData);
      if (parsed.token && parsed.user) {
        dispatch(setUserFromToken(parsed));
        navigate("/", { replace: true });
      }
    }
  }, [dispatch, navigate]);

  // Handle Google OAuth callback
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const email = urlParams.get('email');
    const name = urlParams.get('name');
    
    if (token && email) {
      // Google OAuth callback - user returned with token
      const user = {
        id: Date.now(), // Demo ID
        email: email,
        username: email,
        name: name || email,
        is_staff: false,
        is_superuser: false,
      };
      
      dispatch(setUserFromToken({ token, user }));
      toast.success("Google login successful!");
      
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
      
      // Redirect to home page after Google login
      const redirectTo = location.state?.from || "/";
      navigate(redirectTo, { replace: true });
    }
  }, [dispatch, navigate, location.state]);


  // Countdown timer
  useEffect(() => {
    let interval;
    if (timer > 0) interval = setInterval(() => setTimer(prev => prev - 1), 1000);
    return () => clearInterval(interval);
  }, [timer]);

  useEffect(() => {
    if (otpSent && otpInputRef.current) otpInputRef.current.focus();
  }, [otpSent]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const sendOtp = async (e) => {
    e.preventDefault();
    if (!formData.email) return toast.error("Enter email");
    setLoading(true);
    try {
      const res = await api.post("/auth/send-otp", { email: formData.email });
      if (res.data.success) {
        toast.success("OTP sent successfully!");
        setOtpSent(true);
        setTimer(30);
      } else toast.error(res.data.message || "Failed to send OTP");
    } catch (err) {
      console.error(err);
      toast.error(err.response?.data?.message || "Failed to send OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!otp) return toast.error("Enter OTP");
    setLoading(true);
    try {
      const res = await dispatch(loginUser({ email: formData.email, otp }));
      if (!res.error) {
        toast.success("Login successful!");
        const redirectTo = location.state?.from || "/";
        navigate(redirectTo, { replace: true });
      } else toast.error(res.payload || "Invalid OTP");
    } catch (err) {
      toast.error("Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    // Redirect to backend Google OAuth endpoint
    // This will redirect to Google's actual OAuth page
    window.location.href = "http://localhost:5000/api/auth/google";
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <Toaster position="top-right" />
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        {!otpSent ? (
          <form onSubmit={sendOtp} className="space-y-4">
            <input
              type="email"
              placeholder="Enter email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-3 border rounded-xl"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-500 text-white p-3 rounded-xl"
            >
              {loading ? "Sending OTP..." : "Send OTP"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleLogin} className="space-y-4">
            <input
              ref={otpInputRef}
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full p-3 border rounded-xl"
            />
            <div className="flex justify-between text-sm text-gray-500">
              {timer > 0 ? `Resend in ${timer}s` : <button onClick={sendOtp}>Resend OTP</button>}
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-500 text-white p-3 rounded-xl"
            >
              {loading ? "Verifying..." : "Verify & Login"}
            </button>
          </form>
        )}

        <div className="flex items-center my-4">
          <div className="flex-grow h-px bg-gray-300"></div>
          <span className="px-3 text-gray-500 text-sm">OR</span>
          <div className="flex-grow h-px bg-gray-300"></div>
        </div>
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 border border-gray-300 py-3 rounded-xl hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FcGoogle size={22} /> 
          {loading ? "Signing in..." : "Continue with Google"}
        </button>
      </div>
    </div>
  );
}
