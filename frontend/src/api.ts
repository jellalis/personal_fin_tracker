const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type Category =
  | "food"
  | "transport"
  | "shopping"
  | "entertainment"
  | "bills"
  | "salary"
  | "other";

export interface Transaction {
  id: number;
  title: string;
  amount: number; // positive = income, negative = expense
  category: Category;
  date: string; // ISO date "YYYY-MM-DD"
}

export interface Summary {
  balance: number;
  income: number;
  expense: number;
  currency: string;
}

// --- Auth helpers -----------------------------------------------------------

// Saves the JWT token to localStorage so it persists across page refreshes
export function saveToken(token: string) {
  localStorage.setItem("token", token);
}

// Reads the token back — returns null if not logged in
export function getToken(): string | null {
  return localStorage.getItem("token");
}

// Removes the token — effectively logs the user out
export function clearToken() {
  localStorage.removeItem("token");
}

export function isLoggedIn(): boolean {
  return !!getToken();
}

// --- Core request helper ----------------------------------------------------

// Every API call goes through here — attaches JWT token to the Authorization header
// Backend requires "Authorization: Bearer <token>" for all protected routes
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...init,
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json() as Promise<T>;
}

// --- Category mapping -------------------------------------------------------

// Maps frontend Category strings to backend category names (as seeded in DB)
// "other" maps to null — backend allows NULL category_id (no category)
const CATEGORY_NAME_MAP: Record<Category, string | null> = {
  food:          "food",
  transport:     "transport",
  shopping:      "shopping",
  entertainment: "entertainment",
  bills:         "bills",
  salary:        "salary",
  other:         null,
};

// --- Data shape transformer -------------------------------------------------

// Converts a backend transaction to the shape the frontend expects
// Backend: { amount: "18.5", type: "expense", description: "Ramen", transaction_date: "2026-06-27", category_id: 1 }
// Frontend: { amount: -18.5, title: "Ramen", date: "2026-06-27", category: "food" }
function toFrontend(
  tx: Record<string, unknown>,
  idToName: Record<number, Category>
): Transaction {
  const rawAmount = parseFloat(tx.amount as string);
  const isExpense = tx.type === "expense";
  return {
    id:       tx.id as number,
    title:    (tx.description as string) ?? "",
    amount:   isExpense ? -rawAmount : rawAmount,
    category: idToName[tx.category_id as number] ?? "other",
    date:     (tx.transaction_date as string) ?? "",
  };
}

// --- Public API object ------------------------------------------------------

export const api = {
  // Auth: POST /auth/login with form data (FastAPI OAuth2 expects URLSearchParams, not JSON)
  login: async (email: string, password: string): Promise<void> => {
    const form = new URLSearchParams({ username: email, password });
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form.toString(),
    });
    if (!res.ok) throw new Error("Invalid credentials");
    const data = await res.json();
    saveToken(data.access_token); // store token so all future requests include it
  },

  // Summary: balance, income, expense totals for the logged-in user
  getSummary: () => request<Summary>("/summary"),

  // List: fetch transactions + categories in parallel, then map category_id → name
  listTransactions: async (): Promise<Transaction[]> => {
    const [rawTxs, cats] = await Promise.all([
      request<Record<string, unknown>[]>("/transactions"),
      request<{ id: number; name: string }[]>("/categories"),
    ]);
    const idToName = Object.fromEntries(cats.map((c) => [c.id, c.name as Category]));
    return rawTxs.map((tx) => toFrontend(tx, idToName));
  },

  // Create: transform frontend shape → backend shape before posting
  createTransaction: async (tx: Omit<Transaction, "id">): Promise<Transaction> => {
    const cats = await request<{ id: number; name: string }[]>("/categories");
    const nameToId = Object.fromEntries(cats.map((c) => [c.name, c.id]));
    const idToName = Object.fromEntries(cats.map((c) => [c.id, c.name as Category]));

    const backendName = CATEGORY_NAME_MAP[tx.category];
    const category_id = backendName ? (nameToId[backendName] ?? null) : null;

    const raw = await request<Record<string, unknown>>("/transactions", {
      method: "POST",
      body: JSON.stringify({
        description:      tx.title,
        amount:           Math.abs(tx.amount),
        type:             tx.amount < 0 ? "expense" : "income",
        transaction_date: tx.date,
        category_id,
      }),
    });
    return toFrontend(raw, idToName);
  },

  // Delete: backend returns the deleted object, frontend expects { ok: true }
  deleteTransaction: async (id: number): Promise<{ ok: boolean }> => {
    await request<unknown>(`/transactions/${id}`, { method: "DELETE" });
    return { ok: true };
  },
};
