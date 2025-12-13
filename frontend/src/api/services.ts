import { apiClient } from './client';
import type {
  User,
  UserCreate,
  UserUpdate,
  LoginRequest,
  TokenResponse,
  Group,
  GroupCreate,
  GroupWithMembers,
  AddMemberRequest,
  Expense,
  ExpenseCreate,
  BalanceSummary,
} from '../types';

// Authentication services
export const authService = {
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/auth/login', credentials);
    apiClient.setToken(response.access_token);
    return response;
  },

  async signup(userData: UserCreate): Promise<User> {
    return apiClient.post<User>('/api/auth/signup', userData);
  },

  logout(): void {
    apiClient.clearToken();
  },

  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  },
};

// User services
export const userService = {
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/api/users/me');
  },

  async updateProfile(userData: UserUpdate): Promise<User> {
    return apiClient.put<User>('/api/users/me', userData);
  },
};

// Group services
export const groupService = {
  async createGroup(groupData: GroupCreate): Promise<Group> {
    return apiClient.post<Group>('/api/groups', groupData);
  },

  async getGroups(): Promise<Group[]> {
    return apiClient.get<Group[]>('/api/groups');
  },

  async getGroup(groupId: number): Promise<GroupWithMembers> {
    return apiClient.get<GroupWithMembers>(`/api/groups/${groupId}`);
  },

  async addMember(groupId: number, memberData: AddMemberRequest): Promise<{ message: string }> {
    return apiClient.post<{ message: string }>(`/api/groups/${groupId}/members`, memberData);
  },
};

// Expense services
export const expenseService = {
  async createExpense(expenseData: ExpenseCreate): Promise<Expense> {
    return apiClient.post<Expense>('/api/expenses', expenseData);
  },

  async getGroupExpenses(groupId: number): Promise<Expense[]> {
    return apiClient.get<Expense[]>(`/api/expenses/group/${groupId}`);
  },

  async getBalances(groupId: number): Promise<BalanceSummary> {
    return apiClient.get<BalanceSummary>(`/api/expenses/group/${groupId}/balances`);
  },
};
