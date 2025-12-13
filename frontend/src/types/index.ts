// User types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
}

// Auth types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// Group types
export interface Group {
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface GroupCreate {
  name: string;
  description?: string;
}

export interface GroupMember {
  user_id: number;
  username: string;
  joined_at: string;
}

export interface GroupWithMembers extends Group {
  members: GroupMember[];
}

export interface AddMemberRequest {
  user_id: number;
}

// Expense types
export interface Expense {
  id: number;
  group_id: number;
  paid_by_user_id: number;
  amount: number;
  description: string;
  created_at: string;
}

export interface ExpenseCreate {
  group_id: number;
  amount: number;
  description: string;
}

export interface Balance {
  user_id: number;
  username: string;
  balance: number;
}

export interface BalanceSummary {
  group_id: number;
  group_name: string;
  balances: Balance[];
}
