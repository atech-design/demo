// src/slices/servicesSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../api";

// ✅ Fetch services from backend
export const fetchServices = createAsyncThunk("services/fetch", async () => {
  const res = await api.get("/services/");
  return res.data; // backend returns { success, data, pagination }
});

const servicesSlice = createSlice({
  name: "services",
  initialState: {
    services: [],
    categories: ["All", "Laundry", "Home Care", "Accessories"], // default
    activeCategory: "All",
    status: "idle",
    error: null,
  },
  reducers: {
    setCategory: (state, action) => {
      state.activeCategory = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchServices.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchServices.fulfilled, (state, action) => {
        state.status = "succeeded";

        // ✅ Important fix: backend returns { success, data, pagination }
        state.services = action.payload.data;

        // ✅ Generate dynamic categories from backend + default "All"
        const dynamicCats = [...new Set(action.payload.data.map((s) => s.category))];
        state.categories = ["All", ...dynamicCats];
      })
      .addCase(fetchServices.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      });
  },
});

// ✅ Selectors
export const selectFilteredServices = (state) => {
  if (state.services.activeCategory === "All") return state.services.services;
  return state.services.services.filter(
    (s) => s.category === state.services.activeCategory
  );
};

export const selectCategories = (state) => state.services.categories;
export const selectActiveCategory = (state) => state.services.activeCategory;
export const selectServicesStatus = (state) => state.services.status;

export const { setCategory } = servicesSlice.actions;
export default servicesSlice.reducer;
