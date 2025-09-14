import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../api";

// Save auth to localStorage
const saveAuth = (user, token) => {
  localStorage.setItem("smartLaundryUser", JSON.stringify({ user, token }));
};

// Load from localStorage
const loadAuth = () => {
  try {
    const data = localStorage.getItem("smartLaundryUser");
    return data ? JSON.parse(data) : { user: null, token: null };
  } catch {
    return { user: null, token: null };
  }
};

// Async thunk for OTP login
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, otp }, { rejectWithValue }) => {
    try {
      const res = await api.post("/auth/verify-otp", { email, otp }); // ✅ backend endpoint must exist
      const { token, user } = res.data;
      return { token, user };
    } catch (err) {
      return rejectWithValue(err.response?.data?.message || "OTP verification failed");
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    ...loadAuth(),
    status: "idle",
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.status = "idle";
      state.error = null;
      localStorage.removeItem("smartLaundryUser");
      delete api.defaults.headers.common["Authorization"];
    },
    clearError: (state) => {
      state.error = null;
    },
    setUserFromToken: (state, action) => {
      const { token, user } = action.payload;
      state.user = user;
      state.token = token;
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      saveAuth(user, token);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.user = action.payload.user;
        state.token = action.payload.token;
        api.defaults.headers.common["Authorization"] = `Bearer ${action.payload.token}`;
        saveAuth(action.payload.user, action.payload.token);
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { logout, clearError, setUserFromToken } = authSlice.actions;
export default authSlice.reducer;
