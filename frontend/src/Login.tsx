import { useState } from "react";
import { api } from "./api";

// Login form — shown when no JWT token exists in localStorage
// On success: saves token and calls onLogin() to switch to Dashboard
export function Login({ onLogin }: { onLogin: () => void }) {
  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [error,    setError]    = useState<string | null>(null);
  const [loading,  setLoading]  = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.login(email, password); // saves token to localStorage internally
      onLogin();                         // tell parent: switch to Dashboard
    } catch {
      setError("Wrong email or password. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      {/* faint kanji watermark — same as Dashboard */}
      <div aria-hidden className="pointer-events-none fixed inset-0 flex items-center justify-center overflow-hidden">
        <span className="font-display select-none text-[40vw] leading-none text-ink/[0.03]">忍</span>
      </div>

      <div className="relative w-full max-w-sm">
        <div className="scroll-card p-8">
          {/* Header */}
          <div className="mb-8 text-center">
            <div className="stamp mx-auto mb-4 flex h-14 w-14 items-center justify-center bg-primary text-primary-foreground">
              <span className="font-display text-3xl">蛙</span>
            </div>
            <h1 className="font-display text-2xl">Gama Wallet</h1>
            <p className="mt-1 text-xs text-muted-foreground">Enter your shinobi credentials</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="mb-1 block text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="shinobi@konoha.net"
                required
                className="stamp w-full bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            <div>
              <label className="mb-1 block text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="stamp w-full bg-card px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            {/* Error message */}
            {error && (
              <p className="stamp bg-destructive/10 px-3 py-2 text-xs text-destructive">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="stamp stamp-hover w-full bg-primary px-3 py-2.5 text-sm font-semibold text-primary-foreground disabled:opacity-50"
            >
              {loading ? "Summoning..." : "Enter the village 入村"}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
