import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { apiClient } from '../api/client';

describe('ApiClient', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('Token Management', () => {
    it('should set token in localStorage', () => {
      const token = 'test-token-123';
      apiClient.setToken(token);
      
      expect(localStorage.getItem('auth_token')).toBe(token);
    });

    it('should get token from localStorage', () => {
      const token = 'test-token-456';
      localStorage.setItem('auth_token', token);
      
      expect(apiClient.getToken()).toBe(token);
    });

    it('should clear token from localStorage', () => {
      localStorage.setItem('auth_token', 'test-token');
      apiClient.clearToken();
      
      expect(localStorage.getItem('auth_token')).toBeNull();
    });

    it('should return true when authenticated', () => {
      localStorage.setItem('auth_token', 'test-token');
      
      expect(apiClient.isAuthenticated()).toBe(true);
    });

    it('should return false when not authenticated', () => {
      expect(apiClient.isAuthenticated()).toBe(false);
    });
  });
});
