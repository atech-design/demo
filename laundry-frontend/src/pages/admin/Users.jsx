import React, { useEffect, useState } from "react";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { useSelector } from "react-redux";

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useSelector((state) => state.auth);

  const copyToClipboard = (email) => {
    navigator.clipboard.writeText(email).then(() => {
      toast.success(`Copied ${email} to clipboard`);
    }).catch(() => {
      toast.error("Failed to copy email");
    });
  };

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);

        // Get token from Redux store
        const token = user?.token;
        if (!token) {
          toast.error("Please login to view users");
          return;
        }

        // Fetch real users from backend
        const res = await axios.get("/api/auth/admin/users", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.data.success) {
          setUsers(res.data.data);
        } else {
          toast.error(res.data.message || "Failed to load users");
        }

      } catch (err) {
        console.error("Users Error:", err);
        if (err.response?.status === 403) {
          toast.error("Admin access required");
        } else {
          toast.error("Failed to load users.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [user?.token]);

  return (
    <div className="p-6 min-h-screen bg-gray-50 dark:bg-gray-950">
      <Toaster position="top-right" />

      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Users</h1>

      {loading ? (
        <div className="text-center text-gray-500 dark:text-gray-400">Loading users...</div>
      ) : users.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400">No users found.</p>
      ) : (
        <div className="bg-white dark:bg-gray-800 shadow rounded-xl p-6 overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">User ID</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Name</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">
                  <div className="flex items-center space-x-2">
                    <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-.904.732-1.636 1.636-1.636h.91L12 10.09l9.455-6.27h.909c.904 0 1.636.732 1.636 1.636z"/>
                    </svg>
                    <span>Gmail Address</span>
                  </div>
                </th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Role</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Joined</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {users.map((u) => (
                <tr key={u.id}>
                  <td className="px-4 py-2 text-gray-900 dark:text-gray-100">{u.id}</td>
                  <td className="px-4 py-2 text-gray-900 dark:text-gray-100 font-medium">{u.name}</td>
                  <td className="px-4 py-2">
                    <div className="flex items-center space-x-2">
                      <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-.904.732-1.636 1.636-1.636h.91L12 10.09l9.455-6.27h.909c.904 0 1.636.732 1.636 1.636z"/>
                      </svg>
                      <a 
                        href={`mailto:${u.email}`}
                        className="text-blue-600 dark:text-blue-400 font-medium hover:text-blue-800 dark:hover:text-blue-300 hover:underline transition-colors"
                        title={`Send email to ${u.email}`}
                      >
                        {u.email}
                      </a>
                      <button
                        onClick={() => copyToClipboard(u.email)}
                        className="ml-2 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        title="Copy email address"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                    </div>
                  </td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      u.role === 'Admin' 
                        ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' 
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                    }`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-gray-900 dark:text-gray-100">{u.date_joined}</td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      u.is_active 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                    }`}>
                      {u.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
